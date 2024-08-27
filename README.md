# Brick Structure Visualization and Analysis

This project focuses on generating, visualizing, and evaluating brick structures in different dimensions. The goal is to create various brick layouts and utilize different models to analyze and manipulate these structures.

## Project Structure

```
.
├── data
│   ├── brick_1D_50
│   │   ├── data.json
│   │   ├── images
│   │   │   ├── img_X_bw.png
│   │   │   └── img_X_color.png
│   │   ├── results_gpt-3.5-turbo.json
│   │   ├── results_gpt-4o-2024-08-06.json
│   │   └── results_gpt-4o-mini.json
│   └── brick_2D_50
│       ├── data.json
│       └── images
│           ├── img_X_bw.png
│           └── img_X_color.png
├── notebooks
│   ├── eval_bricks_zeroshot.ipynb
│   └── test_brick_ivan.ipynb
└── scripts
    └── create_bricks_with_drawing.py
```

- **data/**: Contains generated data, images, and model results for different brick dimensions.
- **notebooks/**: Jupyter notebooks for exploring, evaluating, and testing different approaches and models.
- **scripts/**: Python scripts for generating brick structures and visualizing them.

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed. To install the required Python packages, run:

```bash
pip install -r requirements.txt
```

### Installing Jupyter

To run Jupyter notebooks, you may need to install Jupyter:

```bash
pip install jupyter
```

### Usage

#### Generating and Visualizing Brick Structures

The script `create_bricks_with_drawing.py` is used to generate and visualize brick structures.

Run the script with default parameters:

```bash
python scripts/create_bricks_with_drawing.py
```

To customize parameters such as the number of bricks, dimensions, and other attributes, use command-line options. To view all available options, use the `-h` or `--help` flag:

```bash
python scripts/create_bricks_with_drawing.py --help
```

Example with custom parameters:

```bash
python scripts/create_bricks_with_drawing.py --num-bricks 100 --dimension 3
```

#### Jupyter Notebooks

- **eval_bricks_zeroshot.ipynb**: Evaluates different models for brick structure manipulation.
- **test_brick_ivan.ipynb**: Runs prompts testing LLM reasoning with different brick data.

To run the notebooks, navigate to the `notebooks` directory and open the desired notebook using Jupyter:

```bash
jupyter notebook
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to all the contributors and the open-source community for their support and tools.
