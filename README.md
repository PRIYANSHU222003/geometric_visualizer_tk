# 🎨 2D Geometric Transformations Visualizer

A Python desktop application built using **Tkinter** and **NumPy** that demonstrates fundamental **2D geometric transformations** in Computer Graphics. The application provides an interactive graphical interface where users can apply various transformations to a square and visualize the results in real time.

---

## 📌 Features

- Interactive graphical user interface (GUI)
- Cartesian coordinate system with grid
- Displays both:
  - Original Shape (Blue Dashed)
  - Transformed Shape (Red Solid)
- Supports multiple geometric transformations:
  - Translation
  - Scaling
  - Rotation
  - Reflection
  - Shearing
- Transformation about arbitrary pivot points
- Undo last transformation
- Reset shape to original position
- Input validation with error handling

---

## 🛠️ Technologies Used

- Python 3.x
- Tkinter
- NumPy
- Math Library

---

## 📂 Project Structure

```
2D-Geometric-Transformations/
│
├── geometric_visualizer_tk.py     # Main Application
├── README.md                      # Project Documentation
└── requirements.txt               # Dependencies (Optional)
```

---

## 📖 Supported Transformations

### 1. Translation

Moves the object along the X and Y axes.

**Parameters**

- Tx → Horizontal Shift
- Ty → Vertical Shift

---

### 2. Scaling

Resizes the object with respect to a pivot point.

**Parameters**

- Sx → Scale in X direction
- Sy → Scale in Y direction
- Px → Pivot X
- Py → Pivot Y

---

### 3. Rotation

Rotates the object around any specified pivot.

**Parameters**

- Angle (Degrees)
- Rx → Pivot X
- Ry → Pivot Y

---

### 4. Reflection

Reflects the object about:

- X-axis
- Y-axis
- Line y = x

---

### 5. Shearing

Skews the object in X and/or Y directions.

**Parameters**

- Shx → X Shear
- Shy → Y Shear

---

## 📊 Application Workflow

```
Launch Application
        │
        ▼
Display Initial Square
        │
        ▼
Select Transformation
        │
        ▼
Enter Parameters
        │
        ▼
Apply Transformation
        │
        ▼
Visualize Result
        │
        ▼
Undo / Reset (Optional)
```

---

## ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/2D-Geometric-Transformations.git

cd 2D-Geometric-Transformations
```

Install the required package:

```bash
pip install numpy
```

Tkinter is included with most standard Python installations.

---

## ▶️ Running the Application

Run the Python file:

```bash
python geometric_visualizer_tk.py
```

The GUI window will open automatically.

---

## 🖥️ User Interface

The application consists of:

- Drawing Canvas
- Cartesian Coordinate System
- Transformation Selection Panel
- Parameter Input Fields
- Apply Transformation Button
- Reset Button
- Undo Button
- Status Bar

---

## 📚 Mathematical Concepts Used

The application uses **Homogeneous Coordinates (3×3 Transformation Matrices)** to perform transformations.

Implemented matrices include:

- Translation Matrix
- Scaling Matrix
- Rotation Matrix
- Reflection Matrix
- Shearing Matrix

This allows multiple transformations to be performed using matrix multiplication.

---

## 🎯 Learning Objectives

This project helps understand:

- Computer Graphics fundamentals
- Matrix transformations
- Homogeneous coordinates
- Coordinate system mapping
- GUI development using Tkinter
- Object-oriented programming in Python

---

## 🚀 Future Improvements

- Draw custom polygons
- Zoom In / Zoom Out
- Animation of transformations
- Save transformed image
- Support multiple objects
- 3D transformations
- Dark mode interface
- Keyboard shortcuts

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.
