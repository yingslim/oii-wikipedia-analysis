import argparse
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup
from config import *
from tqdm import tqdm

def parse_revision_xml(xml_content: str, include_text: bool = False) -> dict:
    """Parse a single revision XML string into a dictionary."""
    soup = BeautifulSoup(xml_content, "lxml-xml")
    revision = soup.find("revision")
    
    # Extract contributor information safely
    contributor = revision.find("contributor")
    if contributor:
        username = contributor.find("username")
        username = username.text if username else None
        userid = contributor.find("id")
        userid = userid.text if userid else None
    else:
        username = None
        userid = None
    
    # Find text content
    text_elem = revision.find("text")
    text_content = text_elem.text if text_elem else ""
    
    # Extract basic revision information
    data = {
        'revision_id': revision.find("id").text if revision.find("id") else None,
        'timestamp': revision.find("timestamp").text if revision.find("timestamp") else None,
        'username': username,
        'userid': userid,
        'comment': revision.find("comment").text if revision.find("comment") else None,  
        'text_length': len(text_content)
    }
    
    # Optionally include the full text content
    if include_text:
        data['text'] = text_content
    
    return data

def process_article_directory(article_dir: Path, batch_size: int = 1000, include_text: bool = False) -> pd.DataFrame:
    """Process all revisions for an article into a single DataFrame."""
    # Collect all XML files for this article
    xml_files = []
    for year_dir in article_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for day_dir in month_dir.iterdir():
                if not day_dir.is_dir():
                    continue
                xml_files.extend(day_dir.glob("*.xml"))
    
    if not xml_files:
        return None
    
    # Process files in batches
    dataframes = []
    for i in tqdm(range(0, len(xml_files), batch_size),
                 desc=f"Processing {article_dir.name}",
                 unit="batch"):
        batch = xml_files[i:i + batch_size]
        revision_data = []
        
        for file_path in batch:
            try:
                xml_content = file_path.read_text(encoding='utf-8')
                data = parse_revision_xml(xml_content, include_text)
                # Add file path information
                data['year'] = file_path.parent.parent.parent.name
                data['month'] = file_path.parent.parent.name
                data['day'] = file_path.parent.name
                revision_data.append(data)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        if revision_data:
            dataframes.append(pd.DataFrame(revision_data))
    
    if not dataframes:
        return None
    
    # Combine all batches and sort
    final_df = pd.concat(dataframes, ignore_index=True)
    final_df['timestamp'] = pd.to_datetime(final_df['timestamp'])
    return final_df.sort_values('timestamp', ascending=False)

def print_summary(df: pd.DataFrame, article_name: str, include_text: bool):
    """Print summary statistics for an article's DataFrame."""
    print(f"\nSummary for {article_name}:")
    print(f"Total revisions: {len(df)}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Unique contributors: {df['username'].nunique()}")
    print(f"Average text length: {df['text_length'].mean():.1f} characters")
    if include_text:
        memory_usage = df['text'].memory_usage(deep=True) / (1024 * 1024)  # Convert to MB
        print(f"Text content memory usage: {memory_usage:.1f} MB")

def main(data_dir: Path, output_dir: Path, batch_size: int = 1000, include_text: bool = False):
    """
    Process all article directories into separate DataFrames.
    Creates one feather file per article.
    """
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing with {'text content' if include_text else 'text length only'}")
    
    for article_dir in data_dir.iterdir():
        if not article_dir.is_dir():
            continue
        
        df = process_article_directory(article_dir, batch_size, include_text)
        
        if df is not None:
            output_path = output_dir / f"{article_dir.name}.feather"
            df.to_feather(output_path)
            print_summary(df, article_dir.name, include_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Wikipedia revision XMLs to DataFrames",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default= DATA_DIR,
        help="Directory containing article revision directories",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DATA_DIR+"/DataFrames",
        help="Directory to save DataFrame files",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of files to process in each batch",
    )
    parser.add_argument(
        "--include-text",
        action="store_true",
        help="Include full text content in the DataFrame (significantly increases file size)",
    )
    args = parser.parse_args()
    main(args.data_dir, args.output_dir, args.batch_size, args.include_text)
