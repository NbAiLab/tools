import argparse
import pandas as pd
from pandarallel import pandarallel
import logging
import json
import os

pandarallel.initialize(progress_bar=False)  # Initialize pandarallel

def main(input_file, norbench_file, translate_output_folder, detect_output_folder):
    logging.basicConfig(level=logging.INFO)

    # Ensure output folders exist
    os.makedirs(translate_output_folder, exist_ok=True)
    os.makedirs(detect_output_folder, exist_ok=True)

    # Read input_file
    logging.info("Reading input_file...")
    data = pd.read_csv(input_file, sep='\t', names=['date', 'nob', 'nno'], usecols=['nob', 'nno'])
    initial_size = len(data)
    logging.info(f"Size of data: {initial_size:,}")

    # Perform general deduplication
    logging.info("Performing general deduplication...")
    data.drop_duplicates(subset=['nob', 'nno'], keep='first', inplace=True)
    dedup_size = len(data)
    logging.info(f"Size of data after general deduplication: {dedup_size:,}")

    # Remove lines with empty cells
    logging.info("Removing lines with empty cells...")
    data = data.dropna(subset=['nob', 'nno'])
    data = data[(data['nob'] != "") & (data['nno'] != "")]
    after_removal_size = len(data)
    logging.info(f"Size of data after removing empty cells: {after_removal_size:,}")

    # Shuffle and reset index
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Create data splits
    main_train_split = data.iloc[:800000]
    main_devtest_split = data.iloc[800000:]

    # Save translate datasets
    save_translate_dataset(main_train_split, 'train', translate_output_folder)
    save_translate_dataset(main_devtest_split.iloc[:1000], 'dev', translate_output_folder)
    save_translate_dataset(main_devtest_split.iloc[-1000:], 'test', translate_output_folder)
    
    # Save detect datasets
    save_detect_dataset(main_train_split, 'train', detect_output_folder)
    save_detect_dataset(main_devtest_split.iloc[:1000], 'dev', detect_output_folder)
    save_detect_dataset(main_devtest_split.iloc[-1000:], 'test', detect_output_folder)

    logging.info("Operation completed.")

def save_translate_dataset(df, name, folder):
    tsv_path = os.path.join(folder, f"{name}.tsv")
    jsonl_path = os.path.join(folder, f"{name}.jsonl")

    df.to_csv(tsv_path, sep='\t', header=False, index=False)
    logging.info(f"Saved {len(df):,} lines to {tsv_path}")

    with open(jsonl_path, 'w') as f:
        for _, row in df.iterrows():
            line = json.dumps({'nbo': row['nob'], 'nno': row['nno']})
            f.write(line + '\n')

    logging.info(f"Saved {len(df):,} lines to {jsonl_path}")

def save_detect_dataset(df, name, folder):
    melted_df = pd.melt(df, value_vars=['nob', 'nno'], var_name='language', value_name='text')

    # Shuffle and reset index
    melted_df = melted_df.sample(frac=1, random_state=42).reset_index(drop=True)

    tsv_path = os.path.join(folder, f"{name}.tsv")
    jsonl_path = os.path.join(folder, f"{name}.jsonl")

    melted_df.to_csv(tsv_path, sep='\t', header=False, index=False)
    logging.info(f"Saved {len(melted_df):,} lines to {tsv_path}")

    with open(jsonl_path, 'w') as f:
        for _, row in melted_df.iterrows():
            line = json.dumps({'text': row['text'], 'language': row['language']})
            f.write(line + '\n')

    logging.info(f"Saved {len(melted_df):,} lines to {jsonl_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and deduplicate TSV files.')
    parser.add_argument('--input_file', required=True, help='Path to the input TSV file.')
    parser.add_argument('--norbench_file', required=True, help='Path to the norbench TSV file.')
    parser.add_argument('--translate_output_folder', default='translate', help='Folder to save the translate datasets.')
    parser.add_argument('--detect_output_folder', default='detect', help='Folder to save the detect datasets.')

    args = parser.parse_args()
    main(args.input_file, args.norbench_file, args.translate_output_folder, args.detect_output_folder)
