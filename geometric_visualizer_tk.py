

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
from typing import List, Tuple, Optional


class TransformationMatrix:
  
    
    @staticmethod
    def translation(tx: float, ty: float) -> np.ndarray:
       
        return np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=float)
    
    @staticmethod
    def scaling(sx: float, sy: float, px: float = 0, py: float = 0) -> np.ndarray:
       
        # Translate to origin, scale, translate back
        T1 = TransformationMatrix.translation(-px, -py)
        S = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ], dtype=float)
        T2 = TransformationMatrix.translation(px, py)
        
        return T2 @ S @ T1
    
    @staticmethod
    def rotation(angle_deg: float, rx: float = 0, ry: float = 0) -> np.ndarray:
       
        # Convert to radians
        theta = math.radians(angle_deg)
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        
        # Translate to origin, rotate, translate back
        T1 = TransformationMatrix.translation(-rx, -ry)
        R = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ], dtype=float)
        T2 = TransformationMatrix.translation(rx, ry)
        
        return T2 @ R @ T1
    
    @staticmethod
    def reflection(axis: str) -> np.ndarray:
      
        if axis.lower() == 'x':
            # Reflect across X-axis
            return np.array([
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
            ], dtype=float)
        elif axis.lower() == 'y':
            # Reflect across Y-axis
            return np.array([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ], dtype=float)
        elif axis.lower() == 'xy':
            # Reflect across line y=x
            return np.array([
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]
            ], dtype=float)
        else:
            raise ValueError(f"Invalid reflection axis: {axis}")
    
    @staticmethod
    def shearing(shx: float = 0, shy: float = 0) -> np.ndarray:
        
        return np.array([
            [1, shx, 0],
            [shy, 1, 0],
            [0, 0, 1]
        ], dtype=float)


class DrawingCanvas(tk.Canvas):
  
    
    def __init__(self, parent, width=600, height=600, **kwargs):
        super().__init__(parent, width=width, height=height, bg='white', **kwargs)
        self.canvas_width = width
        self.canvas_height = height
        self.origin_x = width // 2
        self.origin_y = height // 2
        
        self.draw_coordinate_system()
    
    def draw_coordinate_system(self):
        # Draw X-axis (horizontal)
        self.create_line(0, self.origin_y, self.canvas_width, self.origin_y,
                        fill='gray', width=1, arrow=tk.LAST)
        self.create_text(self.canvas_width - 20, self.origin_y - 15, 
                        text='X', fill='gray', font=('Arial', 10, 'bold'))
        
        # Draw Y-axis (vertical)
        self.create_line(self.origin_x, self.canvas_height, self.origin_x, 0,
                        fill='gray', width=1, arrow=tk.LAST)
        self.create_text(self.origin_x + 15, 20,
                        text='Y', fill='gray', font=('Arial', 10, 'bold'))
        
        # Draw origin label
        self.create_text(self.origin_x - 15, self.origin_y + 15,
                        text='O', fill='gray', font=('Arial', 10, 'bold'))
        
        # Draw grid lines (optional, lighter)
        grid_spacing = 50
        for i in range(0, self.canvas_width, grid_spacing):
            self.create_line(i, 0, i, self.canvas_height, fill='lightgray', width=1)
        for i in range(0, self.canvas_height, grid_spacing):
            self.create_line(0, i, self.canvas_width, i, fill='lightgray', width=1)
    
    def math_to_canvas(self, x: float, y: float) -> Tuple[float, float]:
    
        canvas_x = self.origin_x + x
        canvas_y = self.origin_y - y  # Flip Y-axis
        return canvas_x, canvas_y
    
    def canvas_to_math(self, canvas_x: float, canvas_y: float) -> Tuple[float, float]:
   
        x = canvas_x - self.origin_x
        y = self.origin_y - canvas_y  # Flip Y-axis
        return x, y
    
    def draw_polygon(self, vertices: np.ndarray, color='red', 
                    width=2, dash=None, tag='polygon'):
       
        # Convert vertices to canvas coordinates
        points = []
        for vertex in vertices:
            x, y = vertex[0], vertex[1]
            canvas_x, canvas_y = self.math_to_canvas(x, y)
            points.extend([canvas_x, canvas_y])
        
        # Draw the polygon
        if len(points) >= 4:
            self.create_polygon(points, outline=color, fill='', 
                              width=width, dash=dash, tags=tag)
    
    def clear_polygons(self):
        """Clear all drawn polygons."""
        self.delete('original')
        self.delete('transformed')


class GeometricVisualizerApp(tk.Tk):
  
    
    def __init__(self):
        super().__init__()
        
        self.title("2D Geometric Transformations Visualizer")
        self.geometry("900x650")
        self.resizable(False, False)
        
        # Initialize state
        self.initial_vertices = self._create_initial_square()
        self.current_vertices = self.initial_vertices.copy()
        self.history = []  # For undo functionality
        
        # Create UI
        self._create_widgets()
        self._update_parameter_inputs()
        
        # Draw initial shapes
        self.draw_shapes()
    
    def _create_initial_square(self) -> np.ndarray:
        """
        Create the initial square in homogeneous coordinates.
        Square centered at (0, 0) with size 100 in mathematical coordinates.
        
        Returns:
            Nx3 numpy array of vertices
        """
        # Square vertices (counter-clockwise from bottom-left)
        vertices = np.array([
            [-50, -50, 1],  # Bottom-left
            [50, -50, 1],   # Bottom-right
            [50, 50, 1],    # Top-right
            [-50, 50, 1]    # Top-left
        ], dtype=float)
        
        return vertices
    
    def _create_widgets(self):
        """Create and layout all UI widgets."""
        # Main container
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Canvas
        canvas_frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
        canvas_frame.grid(row=0, column=0, padx=(0, 10), sticky='nsew')
        
        self.canvas = DrawingCanvas(canvas_frame, width=600, height=600)
        self.canvas.pack()
        
        # Right panel - Controls
        control_frame = tk.Frame(main_frame, width=250)
        control_frame.grid(row=0, column=1, sticky='nsew')
        control_frame.grid_propagate(False)
        
        # Transformation selection
        transform_frame = tk.LabelFrame(control_frame, text="Transformation Type", 
                                       padx=10, pady=10)
        transform_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.transformation_var = tk.StringVar(value="Translation")
        transformations = ["Translation", "Scaling", "Rotation", "Reflection", "Shearing"]
        
        self.transform_combo = ttk.Combobox(transform_frame, 
                                           textvariable=self.transformation_var,
                                           values=transformations,
                                           state='readonly',
                                           width=20)
        self.transform_combo.pack()
        self.transform_combo.bind('<<ComboboxSelected>>', 
                                 lambda e: self._update_parameter_inputs())
        
        # Parameters frame
        self.params_frame = tk.LabelFrame(control_frame, text="Parameters", 
                                         padx=10, pady=10)
        self.params_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Container for dynamic parameter inputs
        self.param_widgets = {}
        
        # Action buttons
        button_frame = tk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(button_frame, text="Apply Transformation", 
                 command=self.apply_transformation,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(fill=tk.X, pady=2)
        
        tk.Button(button_frame, text="Reset Shape", 
                 command=self.reset_shape,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(fill=tk.X, pady=2)
        
        tk.Button(button_frame, text="Undo Last", 
                 command=self.undo_last,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(fill=tk.X, pady=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_frame = tk.Frame(control_frame, relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(status_frame, textvariable=self.status_var, 
                anchor=tk.W, padx=5).pack(fill=tk.X)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        main_frame.rowconfigure(0, weight=1)
    
    def _update_parameter_inputs(self):
        """Update parameter input fields based on selected transformation."""
        # Clear existing parameter widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.param_widgets.clear()
        
        transform = self.transformation_var.get()
        
        if transform == "Translation":
            self._create_param_entry("Tx (X-shift):", "tx", "0")
            self._create_param_entry("Ty (Y-shift):", "ty", "0")
            
        elif transform == "Scaling":
            self._create_param_entry("Sx (X-scale):", "sx", "1.0")
            self._create_param_entry("Sy (Y-scale):", "sy", "1.0")
            self._create_param_entry("Px (pivot X):", "px", "0")
            self._create_param_entry("Py (pivot Y):", "py", "0")
            
        elif transform == "Rotation":
            self._create_param_entry("Angle (degrees):", "angle", "0")
            self._create_param_entry("Rx (pivot X):", "rx", "0")
            self._create_param_entry("Ry (pivot Y):", "ry", "0")
            
        elif transform == "Reflection":
            tk.Label(self.params_frame, text="Reflection Axis:").pack(anchor=tk.W)
            axis_var = tk.StringVar(value="X-axis")
            self.param_widgets['axis'] = axis_var
            
            for axis_option in ["X-axis", "Y-axis", "Line y=x"]:
                tk.Radiobutton(self.params_frame, text=axis_option, 
                             variable=axis_var, value=axis_option).pack(anchor=tk.W)
            
        elif transform == "Shearing":
            self._create_param_entry("Shx (X-shear):", "shx", "0")
            self._create_param_entry("Shy (Y-shear):", "shy", "0")
    
    def _create_param_entry(self, label: str, key: str, default: str):
        """Helper to create a labeled entry field."""
        frame = tk.Frame(self.params_frame)
        frame.pack(fill=tk.X, pady=2)
        
        tk.Label(frame, text=label, width=15, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=10)
        entry.insert(0, default)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.param_widgets[key] = entry
    
    def _get_param_value(self, key: str, default: float = 0.0) -> float:
        """Safely get a parameter value with validation."""
        try:
            widget = self.param_widgets.get(key)
            if isinstance(widget, tk.Entry):
                value = float(widget.get())
                return value
            elif isinstance(widget, tk.StringVar):
                return widget.get()
            return default
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid value for parameter '{key}'")
    
    def apply_transformation(self):
        """Apply the selected transformation to the current shape."""
        try:
            # Save current state for undo
            self.history.append(self.current_vertices.copy())
            
            transform = self.transformation_var.get()
            matrix = None
            
            if transform == "Translation":
                tx = self._get_param_value('tx')
                ty = self._get_param_value('ty')
                matrix = TransformationMatrix.translation(tx, ty)
                self.status_var.set(f"Applied: Translation (Tx={tx}, Ty={ty})")
                
            elif transform == "Scaling":
                sx = self._get_param_value('sx', 1.0)
                sy = self._get_param_value('sy', 1.0)
                px = self._get_param_value('px', 0.0)
                py = self._get_param_value('py', 0.0)
                matrix = TransformationMatrix.scaling(sx, sy, px, py)
                self.status_var.set(f"Applied: Scaling (Sx={sx}, Sy={sy})")
                
            elif transform == "Rotation":
                angle = self._get_param_value('angle')
                rx = self._get_param_value('rx', 0.0)
                ry = self._get_param_value('ry', 0.0)
                matrix = TransformationMatrix.rotation(angle, rx, ry)
                self.status_var.set(f"Applied: Rotation ({angle}°)")
                
            elif transform == "Reflection":
                axis_str = self._get_param_value('axis')
                if "X-axis" in axis_str:
                    axis = 'x'
                elif "Y-axis" in axis_str:
                    axis = 'y'
                else:
                    axis = 'xy'
                matrix = TransformationMatrix.reflection(axis)
                self.status_var.set(f"Applied: Reflection ({axis_str})")
                
            elif transform == "Shearing":
                shx = self._get_param_value('shx', 0.0)
                shy = self._get_param_value('shy', 0.0)
                matrix = TransformationMatrix.shearing(shx, shy)
                self.status_var.set(f"Applied: Shearing (Shx={shx}, Shy={shy})")
            
            # Apply transformation
            if matrix is not None:
                self.current_vertices = (matrix @ self.current_vertices.T).T
                self.draw_shapes()
                
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.status_var.set("Error: Invalid input")
            # Restore state if error occurred
            if self.history:
                self.history.pop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred")
            if self.history:
                self.history.pop()
    
    def reset_shape(self):
        """Reset the shape to the initial square."""
        self.current_vertices = self.initial_vertices.copy()
        self.history.clear()
        self.draw_shapes()
        self.status_var.set("Shape reset to initial state")
    
    def undo_last(self):
        """Undo the last transformation."""
        if self.history:
            self.current_vertices = self.history.pop()
            self.draw_shapes()
            self.status_var.set("Undone last transformation")
        else:
            messagebox.showinfo("Undo", "No transformations to undo")
            self.status_var.set("Nothing to undo")
    
    def draw_shapes(self):
        """Draw both the original and transformed shapes on the canvas."""
        self.canvas.clear_polygons()
        
        # Draw original shape (dashed blue)
        self.canvas.draw_polygon(self.initial_vertices, 
                                color='blue', width=2, dash=(5, 3), tag='original')
        
        # Draw transformed shape (solid red)
        self.canvas.draw_polygon(self.current_vertices, 
                                color='red', width=2, tag='transformed')


def main():
    """Main entry point for the application."""
    app = GeometricVisualizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
