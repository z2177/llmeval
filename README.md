
# Model Evaluation and Comparison

This project evaluates and compares the performance of different AI models using a dataset of questions. It leverages the SiliconFlow API to get responses from several models, and then uses the DeepSeek-R1 Pro model to assess the quality of the responses. The results are saved in an Excel file for further analysis.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Results](#results)
- [License](#license)

## Introduction

This project is designed to evaluate and compare the performance of various AI models on a given set of questions. The models evaluated are:

- `deepseek-ai/DeepSeek-V3`
- `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B`

The dataset of questions is read from a `datasets.jsonl` file, and the responses from each model are stored and compared. Finally, the `DeepSeek-R1` model is used to evaluate the quality of each response, and the results are saved to an Excel file.

## Requirements

To run this project, you'll need the following Python packages:

- `jsonlines`
- `requests`
- `pandas`

You can install them using pip:

```bash
pip install jsonlines requests pandas
```

Additionally, you will need access to the SiliconFlow API and a valid token to interact with the API.

## Setup

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/your-repository-name.git
```

2. **Prepare your dataset:**

Place your dataset file (`datasets.jsonl`) in the root directory. It should contain questions in the following format:

```json
{
    "question": "Your question here",
    "answer": "Your answer here",
    "category": "Your category here"
}
```

3. **Prepare your API token:**

Save your API token in a file named `mydata/token` in the `mydata` directory.

4. **Set up the models list:**

You can adjust the list of models to evaluate in the `models` variable inside the script.

## Usage

1. Run the script:

```bash
python evaluate_models.py
```

2. The script will process each question in the dataset, send requests to the API for each model, and store the results.

3. The responses from each model will be compared and evaluated using `DeepSeek-R1`. The evaluation results will be saved to an Excel file (`mydata/model_responses.xlsx`).

## Results

After running the script, an Excel file will be generated (`model_responses.xlsx`) containing the following columns:

- **Question**: The question from the dataset.
- **DeepSeek-V3**: The response from the `DeepSeek-V3` model.
- **DeepSeek-R1-Distill-Llama-70B**: The response from the `DeepSeek-R1-Distill-Llama-70B` model.
- **DeepSeek-R1-Distill-Qwen-32B**: The response from the `DeepSeek-R1-Distill-Qwen-32B` model.
- **DeepSeek-R1-Distill-Qwen-14B**: The response from the `DeepSeek-R1-Distill-Qwen-14B` model.
- **DeepSeek-R1评估**: The evaluation of the responses from the `DeepSeek-R1` model.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
