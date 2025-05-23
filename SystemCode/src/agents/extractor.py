"""
Extractor Agent Script

Purpose:
This script defines and runs the Extractor Agent using the CrewAI framework.
The agent's primary goal is to analyze processed call transcripts (JSON format)
and extract key customer requirements for travel insurance, structuring them
into a validated JSON object based on the TravelInsuranceRequirement Pydantic model.

Input:
- Reads processed transcript JSON files from a specified directory. Each JSON file
  should contain a list of dictionaries, where each dictionary has 'speaker' and
  'dialogue' keys.
- Default input directory: data/transcripts/processed/

Output:
- Generates structured customer requirement JSON files.
- Saves output files to a specified directory.
- Default output directory: data/extracted_customer_requirements/
- Output filename format: requirements_{original_transcript_name_part}.json
  (e.g., requirements_the_anxious_inquirer_20250403_152253.json)

Dependencies:
- Requires a .env file in the project root containing OpenAI API keys:
  - OPENAI_API_KEY
  - OPENAI_MODEL_NAME (optional, defaults to gpt-4o)
- Relies on the TravelInsuranceRequirement model from src.utils.transcript_processing.

Usage:
Run from the project root directory:
  python src/agents/extractor.py

Optional arguments:
  --input_dir PATH   : Specify a different input directory for processed transcripts.
  --output_dir PATH  : Specify a different output directory for requirement files.
"""

import os
import json
import argparse
from pprint import pprint
from dotenv import load_dotenv
from crewai import Agent, Crew, Task
from src.utils.transcript_processing import TravelInsuranceRequirement

# Step 1: Requirement Extraction Agent - Processes Call Transcripts
transcript_analyst = Agent(
    role="Call Transcript Analyst",
    goal="Extract and structure travel insurance customer requirements from call transcripts into a validated JSON object.",
    backstory=(
        "A seasoned customer service analyst specializing in extracting travel insurance requirements from call transcripts. "
        "This agent listens to conversations between customers and service staff, identifies key requirements, and formats "
        "the insights into a structured JSON output that conforms to the TravelInsuranceRequirement model for accurate policy matching."
    ),
    allow_delegation=False,
    verbose=True,
)

# Define the agent task
transcript_analyst_task = Task(
    description="""Analyze the travel insurance call transcript below and extract key customer requirements.
Step 1: Read the transcript carefully and extract all relevant details. For each field in the schema, provide a brief annotation or reference to the specific portion(s) of the transcript where the detail was found.
Step 2: Review your annotations to verify that every extracted detail directly matches the transcript. Resolve any discrepancies or conflicts in the data.
Step 3: Produce a final, validated JSON object that adheres exactly to the TravelInsuranceRequirement schema

If a field is not mentioned in the transcript, use null.

Transcript:
{parsed_transcripts}
""",
    expected_output="A JSON object that matches the TravelInsuranceRequirement model.",
    agent=transcript_analyst,
    output_json=TravelInsuranceRequirement,
)

# Define the crew with agents and tasks
insurance_recommendation_crew = Crew(
    agents=[transcript_analyst], tasks=[transcript_analyst_task], verbose=True
)


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check for OpenAI API Key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is not set. Please add it to your .env file.")

    # Set environment variables for CrewAI (optional if already set globally, but good practice)
    os.environ["OPENAI_API_KEY"] = openai_api_key
    # Ensure the desired model is set, matching the notebook if necessary
    os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    # --- Determine Project Root ---
    # Assuming this script is in src/agents/, project root is two levels up
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))

    # --- Set up argument parser ---
    parser = argparse.ArgumentParser(
        description="Extract travel insurance requirements from transcript JSON files in a directory."
    )
    parser.add_argument(
        "--input_dir",
        default=os.path.join(project_root, "data", "transcripts", "processed"),
        help="Path to the directory containing parsed transcript JSON files.",
    )
    parser.add_argument(
        "--output_dir",
        default=os.path.join(project_root, "data", "extracted_customer_requirements"),
        help="Path to the directory where extracted requirements JSON files will be saved.",
    )
    # Add arguments for single file processing
    parser.add_argument(
        "--input",
        help="Path to a single processed transcript JSON file to extract requirements from.",
    )
    parser.add_argument(
        "--output",
        help="Path to save the extracted requirements JSON file (required if --input is specified).",
    )
    args = parser.parse_args()

    # --- Argument Validation ---
    if args.input and not args.output:
        parser.error("--output is required when --input is specified.")
    if args.output and not args.input:
        parser.error("--input is required when --output is specified.")
    if args.input and (
        args.input_dir != parser.get_default("input_dir")
        or args.output_dir != parser.get_default("output_dir")
    ):
        print(
            "Warning: --input/--output arguments provided. Ignoring --input_dir and --output_dir."
        )

    # --- Decide Mode: Single File or Batch ---
    if args.input and args.output:
        # --- Single File Processing ---
        print(f"Starting single file extraction for: {args.input}")
        if not os.path.isfile(args.input):
            print(f"Error: Input file not found at {args.input}")
            return
        # Ensure output directory exists
        output_dir_single = os.path.dirname(args.output)
        if output_dir_single:
            os.makedirs(output_dir_single, exist_ok=True)

        success = process_single_transcript(args.input, args.output)
        if success:
            print(f"Extraction finished successfully for {args.input}.")
        else:
            print(f"Extraction failed for {args.input}.")
            exit(1)  # Exit with error for single file failure

    else:
        # --- Batch Processing ---
        # Validate input directory for batch mode
        if not os.path.isdir(args.input_dir):
            print(f"Error: Input directory not found at {args.input_dir}")
            return
        # Ensure output directory exists for batch mode
        os.makedirs(args.output_dir, exist_ok=True)

        print(f"Starting batch extraction from: {args.input_dir}")
        print(f"Output will be saved to: {args.output_dir}")
        run_batch_extraction(args.input_dir, args.output_dir)


def process_single_transcript(input_file_path: str, output_file_path: str) -> bool:
    """
    Reads a single processed transcript JSON, runs the extractor crew, and saves the result.

    Args:
        input_file_path: Path to the processed transcript JSON file.
        output_file_path: Path to save the extracted requirements JSON file.

    Returns:
        True if processing and saving were successful, False otherwise.
    """
    filename = os.path.basename(input_file_path)
    print(f"\n--- Processing file: {filename} ---")

    # --- Read and parse the JSON transcript ---
    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            transcript_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_file_path}")
        return False
    except Exception as e:
        print(f"Error reading transcript file {input_file_path}: {e}")
        return False

    # --- Convert the transcript data to a string format for the agent ---
    formatted_transcript = ""
    if isinstance(transcript_data, list) and all(
        isinstance(item, dict) and "speaker" in item and "dialogue" in item
        for item in transcript_data
    ):
        formatted_transcript = "\n".join(
            [f"{msg['speaker']}: {msg['dialogue']}" for msg in transcript_data]
        )
    else:
        print(
            f"Error: Transcript data in {filename} is not in the expected format (list of {{'speaker': ..., 'dialogue': ...}} dictionaries)."
        )
        # Attempt to handle if it's already a string or other format if needed
        if isinstance(transcript_data, str):
            print("Attempting to use raw string data.")
            formatted_transcript = transcript_data  # Assume it's already formatted
        else:
            # Fallback or specific handling for other formats if necessary
            print("Attempting to convert transcript data to string as fallback.")
            try:
                formatted_transcript = str(transcript_data)
            except Exception as str_e:
                print(f"Could not convert transcript data to string: {str_e}")
                return False

    if not formatted_transcript:
        print(f"Error: Could not format transcript from {filename}. Skipping.")
        return False

    # --- Prepare inputs for the crew ---
    input_data = {"parsed_transcripts": formatted_transcript}

    # --- Execute the crew to process the transcript ---
    print("Kicking off the crew...")
    result = None  # Initialize result
    try:
        result = insurance_recommendation_crew.kickoff(inputs=input_data)
        # Print the result
        print("\nExtraction Result:")
        pprint(result)

    except Exception as crew_e:
        print(f"Error during CrewAI kickoff for {filename}: {crew_e}")
        return False

    # --- Save the result to the specified output path ---
    if result:
        try:
            # Save the result dictionary as JSON
            with open(output_file_path, "w", encoding="utf-8") as f:
                # Convert the Pydantic model (result) to a dictionary before saving
                # Check if result is already a dict (sometimes crewai might return dict)
                if isinstance(result, dict):
                    json.dump(result, f, indent=4, ensure_ascii=False)
                elif hasattr(result, "model_dump"):  # Check if it's a Pydantic model
                    json.dump(result.model_dump(), f, indent=4, ensure_ascii=False)
                else:
                    print(
                        f"Warning: Result for {filename} is not a dict or Pydantic model. Attempting to save raw result."
                    )
                    json.dump(
                        str(result), f, indent=4, ensure_ascii=False
                    )  # Save string representation as fallback

            print(f"\nSuccessfully saved extraction results to: {output_file_path}")
            return True

        except Exception as save_e:
            print(f"\nError saving extraction results for {filename}: {save_e}")
            return False
    else:
        print(f"\nNo result generated for {filename}, skipping save.")
        return False


def run_batch_extraction(input_dir: str, output_dir: str):
    """
    Iterates through files in the input directory and processes each transcript.
    """
    processed_count = 0
    failed_count = 0

    # --- Iterate through files in the input directory ---
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".json"):
            input_file_path = os.path.join(input_dir, filename)

            # --- Construct the output filename for batch mode ---
            output_filename = f"requirements_{filename}"  # Default fallback
            base_name = os.path.basename(input_file_path)
            name_part = os.path.splitext(base_name)[0]
            if name_part.startswith("parsed_"):
                name_part = name_part[len("parsed_") :]
            if name_part.startswith("transcript_"):
                name_part = name_part[len("transcript_") :]
            output_filename = f"requirements_{name_part}.json"
            output_file_path = os.path.join(output_dir, output_filename)
            # --- End output filename construction ---

            success = process_single_transcript(input_file_path, output_file_path)
            if success:
                processed_count += 1
            else:
                failed_count += 1

    print(f"\n--- Batch Extraction Finished ---")
    print(f"Successfully processed: {processed_count} files.")
    print(f"Failed attempts: {failed_count} files.")


if __name__ == "__main__":
    main()
