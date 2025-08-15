# Auto-Lecture: Automated Educational Content Generator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com)

An intelligent pipeline that transforms PDF lecture slides into comprehensive educational materials including study notes, transcripts, questions, and key points using OpenAI's GPT models.

## Overview

Auto-Lecture is a three-stage automated system that:

1. **Merges** multiple PDF slide files into a single organized document
2. **Extracts** structured content from PDFs with intelligent text processing
3. **Generates** comprehensive educational materials using AI

## Features

- **PDF Processing**: Automatically merge and organize multiple PDF slide files
- **Smart Content Extraction**: Extract clean, structured text from PDFs with duplicate detection
- **AI-Powered Generation**: Generate multiple types of educational content:
  - Detailed study notes with enhanced headings
  - Natural language lecture transcripts
  - Comprehensive multiple-choice questions with explanations
  - Key testable facts and points
- **Concurrent Processing**: Multi-threaded execution for faster processing
- **Cost Tracking**: Built-in API cost monitoring and optimization
- **Flexible Configuration**: Easily customizable prompts and settings
- **Organized Output**: Clean, structured markdown files for easy consumption

## Web App

A web application for Auto-Lecture is available at [https://github.com/Kisara-k/auto-lecture-app](https://github.com/Kisara-k/auto-lecture-app).

![Auto-Lecture Web App Demo 1](https://github.com/Kisara-k/auto-lecture-app/raw/main/assets/demo/Screenshot_83.png)
![Auto-Lecture Web App Demo 2](https://github.com/Kisara-k/auto-lecture-app/raw/main/assets/demo/Screenshot_85.png)

## Requirements

### Dependencies

```
fitz (PyMuPDF)
openai
python-dotenv
```

### Environment Setup

Create a `.env` file in the project root:

```env
OPENAI_KEY=your_openai_api_key_here
```
## Installation

1. **Clone the repository**:

  ```bash
  git clone <repository-url>
  cd auto-lecture
  ```

2. **Install dependencies**:

  ```bash
  pip install PyMuPDF openai python-dotenv
  ```

3. **Configure environment**:

  - Create `.env` file with your OpenAI API key
  - Adjust settings in `flags.py` (optional)

4. **Prepare slides**:
  - Place PDF files in the `slides/` directory
  - Files should be named with numeric prefixes (e.g., `01 Introduction.pdf`, `02 Advanced Topics.pdf`)

## Usage

### Quick Start

Run the complete pipeline:

```bash
RUN_PIPELINE.bat
```

### Manual Execution

Run individual stages:

```bash
# Stage 1: Merge PDF slides
python 1_merge_slides.py

# Stage 2: Extract content
python 2_extract_content.py

# Stage 3: Generate AI content
python 3_call_api.py
```

### Configuration

Edit `flags.py` to customize behavior:

```python
# Processing range
START, NUM_LECS = 0, 100  # Process lectures 0-99

# AI Model selection
MODEL = "gpt-4.1-mini"    # Available: gpt-4.1, gpt-4.1-mini, gpt-4o, etc.

# Content generation flags
GET_TRANSCRIPTS = True    # Generate lecture transcripts
GET_KEY_POINTS = True     # Extract key testable facts
GET_Q_AND_A = True        # Create questions and answers

# Optimization flags
TRY_REUSE_NOTES = False   # Reuse existing notes to save API calls
IS_BOOK = False           # Adjust prompts for book content vs lectures
```

## Project Structure

```
auto-lecture/
├── 1_merge_slides.py      # PDF merging and bookmark creation
├── 2_extract_content.py   # Content extraction and cleaning
├── 3_call_api.py         # AI content generation
├── config.py             # Core configuration and prompts
├── flags.py              # User-configurable settings
├── RUN_PIPELINE.bat      # Complete pipeline execution
├── slides/               # Input PDF slides directory
├── outputs/              # Generated markdown files
├── Lectures.pdf          # Merged PDF output
├── Lectures.json         # Extracted content JSON
└── README.md            # This file
```

## Pipeline Stages

### Stage 1: PDF Merging (`1_merge_slides.py`)

- Combines multiple PDF files from `slides/` directory
- Creates intelligent bookmarks based on filenames
- Removes existing bookmarks to avoid conflicts
- Handles numeric prefixes intelligently (removes leading zeros)
- Outputs: `Lectures.pdf`

**Key Features**:

- Automatic bookmark generation from filenames
- Smart numeric prefix handling
- Error handling for corrupted PDFs

### Stage 2: Content Extraction (`2_extract_content.py`)

- Extracts structured text from the merged PDF
- Intelligent duplicate content detection
- Advanced text cleaning and normalization
- Table of contents parsing
- Outputs: `Lectures.json`

**Key Features**:

- Smart Text Cleaning: Removes page numbers, headers, and noise
- Duplicate Detection: Avoids processing similar consecutive pages
- Capital Letter Normalization: Fixes ALL-CAPS text blocks
- Unicode Normalization: Converts special characters to ASCII
- Chapter Segmentation: Automatically splits content by headings

### Stage 3: AI Content Generation (`3_call_api.py`)

- Generates comprehensive educational materials using OpenAI's GPT models
- Multi-threaded processing for efficiency
- Cost tracking and rate limit handling
- Flexible content type selection

**Generated Content Types**:

1. Study Notes: Detailed, well-structured notes with:

  - Enhanced headings
  - Clear explanations in accessible language
  - Numbered main sections
  - Comprehensive coverage of all topics

2. Lecture Transcripts: Natural language spoken-form lectures:

  - Conversational, engaging tone
  - Clear topic progression
  - Introductory-level explanations

3. Questions & Answers: Comprehensive assessment materials:

  - 20 multiple-choice questions per lecture
  - Challenging questions requiring deep understanding
  - Detailed explanations for each answer choice
  - Correct answer identification

4. Key Points: Essential testable facts:
  - Structured bullet points
  - Categorization by topic
  - Focus on testable content
  - Organized by topic areas

## Advanced Configuration

### Custom Prompts

The system uses sophisticated prompts defined in `config.py`:

- `system_prompt`: Sets the AI's role and behavior
- `user_prompt_1`: Study notes generation prompt
- `user_prompt_2`: Transcript generation prompt
- `user_prompt_3`: Question generation prompt
- `user_prompt_4`: Answer explanation prompt
- `user_prompt_5`: Key points extraction prompt

### Model Selection and Costs

Supported models with pricing (per 1M tokens):

| Model        | Input | Cached | Output |
| ------------ | ----- | ------ | ------ |
| gpt-4.1      | $2.00 | $0.50  | $8.00  |
| gpt-4.1-mini | $0.40 | $0.10  | $1.60  |
| gpt-4o       | $2.50 | $1.25  | $10.00 |
| gpt-4o-mini  | $0.15 | $0.08  | $0.60  |

### Performance Optimization

- Concurrent Processing: Multiple threads for API calls
- Rate Limit Handling: Automatic retry with exponential backoff
- Content Reuse: Option to reuse existing notes (`TRY_REUSE_NOTES`)
- Selective Generation: Toggle individual content types

## Output Format

Generated files follow this structure:

```markdown
## [Lecture Number] [Title]

[Study Notes](#study-notes)
[Questions](#questions)

### Key Points

[Key testable facts organized by topic]

## Study Notes

[Detailed educational content with enhanced headings]

## Questions

[20 multiple choice questions]

## Answers

[Detailed explanations for each question]
```

## Troubleshooting

### Common Issues

**PDF Processing Errors**:

- Ensure PDFs are not corrupted or password-protected
- Check that files have proper numeric prefixes
- Verify `slides/` directory exists and contains PDF files

**API Errors**:

- Verify OpenAI API key is set correctly in `.env`
- Check API rate limits and usage quotas
- Ensure sufficient account balance

**Content Quality Issues**:

- Adjust model temperature in `3_call_api.py` (default: 0.3)
- Modify prompts in `config.py` for different output styles
- Use higher-tier models for better quality

**Performance Issues**:

- Reduce concurrent threads if hitting rate limits
- Use `TRY_REUSE_NOTES` to avoid regenerating existing content
- Process smaller batches using `START` and `NUM_LECS` settings

## Cost Estimation

Typical costs per lecture (using gpt-4.1-mini):

- Study Notes: ~$0.05-0.10
- Transcript: ~$0.03-0.08
- Questions: ~$0.02-0.05
- Answers: ~$0.03-0.06
- Key Points: ~$0.01-0.03

**Total per lecture**: ~$0.14-0.32

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing
- [OpenAI](https://openai.com/) for GPT models
- Contributors and users providing feedback

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check the troubleshooting section
- Review existing discussions

