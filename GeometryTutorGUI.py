import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import xml.etree.ElementTree as ET
import os

# ===================== OWL ONTOLOGY LOADER =====================
class OWLOntologyLoader:
    """Loads and parses the OWL ontology file"""
    def __init__(self, owl_file_path='geometry_ontology.owl'):
        self.owl_file = owl_file_path
        self.namespaces = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'geo': 'http://www.example.org/geometry#'
        }
        self.shapes_data = {}
        self.formulas = {}
        self.difficulty_levels = {}
        
        if os.path.exists(owl_file_path):
            self.load_ontology()
        else:
            print(f"Warning: {owl_file_path} not found. Using default ontology.")
            self.use_default_ontology()
    
    def load_ontology(self):
        """Parse OWL file and extract shape information"""
        try:
            tree = ET.parse(self.owl_file)
            root = tree.getroot()
            
            # Register namespaces for XPath
            for prefix, uri in self.namespaces.items():
                ET.register_namespace(prefix, uri)
            
            # Extract formulas
            self._extract_formulas(root)
            
            # Extract difficulty levels
            self._extract_difficulty_levels(root)
            
            # Extract shape information
            self._extract_shapes(root)
            
            print("Ontology loaded successfully from OWL file!")
            
        except Exception as e:
            print(f"Error loading ontology: {e}")
            self.use_default_ontology()
    
    def _extract_formulas(self, root):
        """Extract area formulas from OWL"""
        for individual in root.findall('.//{http://www.w3.org/2002/07/owl#}NamedIndividual'):
            about = individual.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            
            if 'AreaFormula' in about:
                formula_name = about.split('#')[-1]
                formula_expr = individual.find('.//{http://www.example.org/geometry#}hasFormulaExpression')
                
                if formula_expr is not None:
                    self.formulas[formula_name] = formula_expr.text
    
    def _extract_difficulty_levels(self, root):
        """Extract difficulty levels from OWL"""
        for individual in root.findall('.//{http://www.w3.org/2002/07/owl#}NamedIndividual'):
            about = individual.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            
            if 'Level' in about and 'Difficulty' not in about:
                level_name = about.split('#')[-1]
                difficulty_value = individual.find('.//{http://www.example.org/geometry#}hasDifficultyValue')
                
                if difficulty_value is not None:
                    self.difficulty_levels[level_name] = int(difficulty_value.text)
    
    def _extract_shapes(self, root):
        """Extract shape information from OWL"""
        shape_types = ['SquareType', 'RectangleType', 'TriangleType', 
                      'CircleType', 'TrapezoidType', 'ParallelogramType']
        
        for individual in root.findall('.//{http://www.w3.org/2002/07/owl#}NamedIndividual'):
            about = individual.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
            shape_name = about.split('#')[-1]
            
            if shape_name in shape_types:
                # Get description
                description_elem = individual.find('.//{http://www.example.org/geometry#}hasDescription')
                description = description_elem.text if description_elem is not None else ""
                
                # Get formula reference
                formula_elem = individual.find('.//{http://www.example.org/geometry#}hasFormula')
                formula_ref = ""
                if formula_elem is not None:
                    formula_ref = formula_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '').split('#')[-1]
                
                # Get difficulty reference
                difficulty_elem = individual.find('.//{http://www.example.org/geometry#}hasDifficulty')
                difficulty = 1
                if difficulty_elem is not None:
                    diff_ref = difficulty_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '').split('#')[-1]
                    difficulty = self.difficulty_levels.get(diff_ref, 1)
                
                # Get shape type
                type_elem = individual.find('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}type')
                shape_class = ""
                if type_elem is not None:
                    shape_class = type_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource', '').split('#')[-1]
                
                # Map shape properties
                properties = self._get_shape_properties(shape_class)
                
                # Store shape data
                clean_name = shape_name.replace('Type', '').lower()
                self.shapes_data[clean_name] = {
                    'description': description,
                    'formula': self.formulas.get(formula_ref, ''),
                    'difficulty': difficulty,
                    'properties': properties,
                    'parent': self._get_parent_class(shape_class)
                }
    
    def _get_shape_properties(self, shape_class):
        """Map shape classes to their required properties"""
        property_map = {
            'Square': ['side'],
            'Rectangle': ['length', 'width'],
            'Triangle': ['base', 'height'],
            'Circle': ['radius'],
            'Trapezoid': ['base1', 'base2', 'height'],
            'Parallelogram': ['base', 'height']
        }
        return property_map.get(shape_class, [])
    
    def _get_parent_class(self, shape_class):
        """Map shape classes to their parent concepts"""
        parent_map = {
            'Square': 'rectangle',
            'Rectangle': 'quadrilateral',
            'Triangle': 'polygon',
            'Circle': 'conic_section',
            'Trapezoid': 'quadrilateral',
            'Parallelogram': 'quadrilateral'
        }
        return parent_map.get(shape_class, 'shape')
    
    def use_default_ontology(self):
        """Fallback to hardcoded ontology if OWL file not found"""
        self.shapes_data = {
            'square': {
                'parent': 'rectangle',
                'properties': ['side'],
                'formula': 'side²',
                'difficulty': 1,
                'description': 'A rectangle with all sides equal'
            },
            'rectangle': {
                'parent': 'quadrilateral',
                'properties': ['length', 'width'],
                'formula': 'length × width',
                'difficulty': 1,
                'description': 'A quadrilateral with four right angles'
            },
            'triangle': {
                'parent': 'polygon',
                'properties': ['base', 'height'],
                'formula': '½ × base × height',
                'difficulty': 2,
                'description': 'A polygon with three sides'
            },
            'circle': {
                'parent': 'conic_section',
                'properties': ['radius'],
                'formula': 'π × radius²',
                'difficulty': 2,
                'description': 'A set of points equidistant from center'
            },
            'trapezoid': {
                'parent': 'quadrilateral',
                'properties': ['base1', 'base2', 'height'],
                'formula': '½ × (base1 + base2) × height',
                'difficulty': 3,
                'description': 'A quadrilateral with one pair of parallel sides'
            },
            'parallelogram': {
                'parent': 'quadrilateral',
                'properties': ['base', 'height'],
                'formula': 'base × height',
                'difficulty': 2,
                'description': 'A quadrilateral with opposite sides parallel'
            }
        }

# ===================== ONTOLOGY DEFINITION =====================
class GeometryOntology:
    """
    Ontology for 2D shapes and area calculation concepts.
    Loads from OWL file or uses default definitions.
    """
    def __init__(self, owl_file='geometry_ontology.owl'):
        loader = OWLOntologyLoader(owl_file)
        self.shapes = loader.shapes_data
        
        self.concepts = {
            'area': 'The amount of space inside a 2D shape',
            'perimeter': 'The distance around a 2D shape',
            'base': 'The bottom side of a shape',
            'height': 'Perpendicular distance from base to top',
            'radius': 'Distance from center to edge of circle'
        }
    
    def get_shape_info(self, shape):
        return self.shapes.get(shape, {})
    
    def get_difficulty_shapes(self, level):
        return [s for s, info in self.shapes.items() if info['difficulty'] == level]
    
    def get_ontology_summary(self):
        """Return summary of loaded ontology"""
        summary = f"Loaded {len(self.shapes)} shapes from ontology:\n"
        for shape, info in self.shapes.items():
            summary += f"  - {shape.capitalize()}: {info['description']}\n"
        return summary

# ===================== PEDAGOGICAL ENGINE =====================
class PedagogicalEngine:
    """Manages learning progression and feedback"""
    def __init__(self, ontology):
        self.ontology = ontology
        self.student_model = {
            'attempts': {},
            'correct': {},
            'current_level': 1
        }
    
    def generate_problem(self, shape):
        info = self.ontology.get_shape_info(shape)
        params = {}
        
        for prop in info['properties']:
            params[prop] = random.randint(2, 15)
        
        return params
    
    def calculate_area(self, shape, params):
        if shape == 'square':
            return params['side'] ** 2
        elif shape == 'rectangle':
            return params['length'] * params['width']
        elif shape == 'triangle':
            return 0.5 * params['base'] * params['height']
        elif shape == 'circle':
            return math.pi * (params['radius'] ** 2)
        elif shape == 'trapezoid':
            return 0.5 * (params['base1'] + params['base2']) * params['height']
        elif shape == 'parallelogram':
            return params['base'] * params['height']
        return 0
    
    def provide_feedback(self, shape, user_answer, correct_answer, params):
        diff = abs(user_answer - correct_answer)
        tolerance = correct_answer * 0.02  # 2% tolerance
        
        if diff <= tolerance:
            return "correct", "🎉 Excellent! Your answer is correct!"
        elif diff <= correct_answer * 0.1:
            return "close", f"Close! The correct answer is {correct_answer:.2f}. Review the formula."
        else:
            info = self.ontology.get_shape_info(shape)
            hint = self.generate_hint(shape, params, info)
            return "incorrect", f"Not quite. {hint}\nCorrect answer: {correct_answer:.2f}"
    
    def generate_hint(self, shape, params, info):
        formula = info['formula']
        if shape == 'square':
            return f"For a square: Area = {formula} = {params['side']}² = {params['side']} × {params['side']}"
        elif shape == 'rectangle':
            return f"For a rectangle: Area = {formula} = {params['length']} × {params['width']}"
        elif shape == 'triangle':
            return f"For a triangle: Area = {formula} = ½ × {params['base']} × {params['height']}"
        elif shape == 'circle':
            return f"For a circle: Area = {formula} ≈ 3.14159 × {params['radius']}²"
        elif shape == 'trapezoid':
            return f"For a trapezoid: Area = {formula} = ½ × ({params['base1']} + {params['base2']}) × {params['height']}"
        elif shape == 'parallelogram':
            return f"For a parallelogram: Area = {formula} = {params['base']} × {params['height']}"
        return "Check the formula and try again."
    
    def update_student_model(self, shape, is_correct):
        if shape not in self.student_model['attempts']:
            self.student_model['attempts'][shape] = 0
            self.student_model['correct'][shape] = 0
        
        self.student_model['attempts'][shape] += 1
        if is_correct:
            self.student_model['correct'][shape] += 1

# ===================== GRAPHICAL USER INTERFACE =====================
class GeometryTutorGUI:
    def __init__(self, root, owl_file='geometry_ontology.owl'):
        self.root = root
        self.root.title("Geometry Area Tutor - OWL-Based ITS")
        self.root.geometry("800x650")
        
        self.ontology = GeometryOntology(owl_file)
        self.engine = PedagogicalEngine(self.ontology)
        
        self.current_shape = None
        self.current_params = None
        self.current_answer = None
        
        self.setup_ui()
        
        # Bind Enter key to submit answer
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
    
    def setup_ui(self):
    # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="🎓 Geometry Area Tutor (OWL-Based)", 
                         font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        # ================= Scrollable Main Container =================
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Use scrollable_frame instead of main for packing widgets
        main = scrollable_frame
        main.config(padx=20, pady=20)
        
        # --- Shape selection ---
        select_frame = tk.LabelFrame(main, text="Select a Shape", font=("Arial", 12, "bold"), padx=10, pady=10)
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.shape_var = tk.StringVar(value="square")
        shapes = list(self.ontology.shapes.keys())
        
        for i, shape in enumerate(shapes):
            rb = tk.Radiobutton(select_frame, text=shape.capitalize(), 
                                variable=self.shape_var, value=shape,
                                font=("Arial", 11))
            rb.grid(row=i//3, column=i%3, sticky=tk.W, padx=10, pady=5)
        
        # --- Problem display ---
        self.problem_frame = tk.LabelFrame(main, text="Current Problem", 
                                           font=("Arial", 12, "bold"), padx=10, pady=10)
        self.problem_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.problem_label = tk.Label(self.problem_frame, text="Click 'New Problem' to start",
                                      font=("Arial", 14), wraplength=700, justify=tk.LEFT)
        self.problem_label.pack(pady=20)
        
        # --- Answer input ---
        answer_frame = tk.Frame(main)
        answer_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(answer_frame, text="Your Answer:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.answer_entry = tk.Entry(answer_frame, font=("Arial", 12), width=15)
        self.answer_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(answer_frame, text="Submit Answer", command=self.check_answer,
                  bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=20, pady=5).pack(side=tk.LEFT)
        
        # --- Feedback ---
        self.feedback_label = tk.Label(main, text="", font=("Arial", 11), 
                                       wraplength=700, justify=tk.LEFT, fg="#2980b9")
        self.feedback_label.pack(pady=10)
        
        # --- Control buttons ---
        btn_frame = tk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="New Problem", command=self.new_problem,
                  bg="#3498db", fg="white", font=("Arial", 11, "bold"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Show Formula", command=self.show_formula,
                  bg="#9b59b6", fg="white", font=("Arial", 11, "bold"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="View Progress", command=self.show_progress,
                  bg="#e67e22", fg="white", font=("Arial", 11, "bold"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Ontology Info", command=self.show_ontology_info,
                  bg="#16a085", fg="white", font=("Arial", 11, "bold"), padx=30, pady=8).pack(side=tk.LEFT, padx=5)
    
    def new_problem(self):
        self.current_shape = self.shape_var.get()
        self.current_params = self.engine.generate_problem(self.current_shape)
        self.current_answer = self.engine.calculate_area(self.current_shape, self.current_params)
        
        info = self.ontology.get_shape_info(self.current_shape)
        
        problem_text = f"Shape: {self.current_shape.upper()}\n\n"
        problem_text += f"Description: {info['description']}\n\n"
        problem_text += "Given:\n"
        
        for prop, value in self.current_params.items():
            problem_text += f"  • {prop.capitalize()}: {value} units\n"
        
        problem_text += f"\nCalculate the area of this {self.current_shape}."
        
        self.problem_label.config(text=problem_text)
        self.feedback_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
    
    def check_answer(self):
        if self.current_answer is None:
            messagebox.showwarning("No Problem", "Please generate a new problem first!")
            return
        
        try:
            user_answer = float(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return
        
        status, feedback = self.engine.provide_feedback(
            self.current_shape, user_answer, self.current_answer, self.current_params
        )
        
        self.engine.update_student_model(self.current_shape, status == "correct")
        
        color = "#27ae60" if status == "correct" else "#e74c3c" if status == "incorrect" else "#f39c12"
        self.feedback_label.config(text=feedback, fg=color)
        
        # Clear entry for next attempt or auto-generate new problem on correct answer
        if status == "correct":
            self.answer_entry.delete(0, tk.END)
    
    def show_formula(self):
        shape = self.shape_var.get()
        info = self.ontology.get_shape_info(shape)
        
        formula_text = f"Shape: {shape.upper()}\n\n"
        formula_text += f"Area Formula: {info['formula']}\n\n"
        formula_text += f"Description: {info['description']}\n\n"
        formula_text += f"Parent Class: {info.get('parent', 'N/A')}\n"
        formula_text += f"Difficulty Level: {info.get('difficulty', 1)}"
        
        messagebox.showinfo("Formula Reference", formula_text)
    
    def show_progress(self):
        model = self.engine.student_model
        
        if not model['attempts']:
            messagebox.showinfo("Progress", "No attempts yet. Start solving problems!")
            return
        
        progress_text = "📊 Your Learning Progress\n\n"
        
        for shape in sorted(model['attempts'].keys()):
            attempts = model['attempts'][shape]
            correct = model['correct'][shape]
            accuracy = (correct / attempts * 100) if attempts > 0 else 0
            
            progress_text += f"{shape.capitalize()}: {correct}/{attempts} correct ({accuracy:.1f}%)\n"
        
        total_attempts = sum(model['attempts'].values())
        total_correct = sum(model['correct'].values())
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        progress_text += f"\n{'='*40}\n"
        progress_text += f"Overall: {total_correct}/{total_attempts} correct ({overall_accuracy:.1f}%)"
        
        messagebox.showinfo("Learning Progress", progress_text)
    
    def show_ontology_info(self):
        """Display information about the loaded ontology"""
        summary = self.ontology.get_ontology_summary()
        summary += f"\nTotal Concepts: {len(self.ontology.concepts)}"
        summary += "\n\nThe system uses OWL (Web Ontology Language) to define:"
        summary += "\n• Shape hierarchies and relationships"
        summary += "\n• Area calculation formulas"
        summary += "\n• Difficulty levels for adaptive learning"
        summary += "\n• Geometric properties and measurements"
        
        messagebox.showinfo("Ontology Information", summary)

# ===================== MAIN =====================
if __name__ == "__main__":
    root = tk.Tk()
    
    # You can specify a different OWL file path here
    owl_file = 'geometry_ontology.owl'
    
    app = GeometryTutorGUI(root, owl_file)
    root.mainloop()