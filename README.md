Here’s a **clean, professional GitHub README.md** tailored for your project and suitable for academic, portfolio, or educational use.

---

# 🎓 Geometry Area Tutor (OWL-Based Intelligent Tutoring System)

An **OWL-driven Intelligent Tutoring System (ITS)** for learning **2D geometry area calculations**, built with **Python and Tkinter**.
The application combines **semantic web technologies (OWL ontologies)** with **pedagogical logic** to provide adaptive, explainable, and interactive learning.

---

## 📌 Features

* 🧠 **Ontology-Driven Learning**

  * Uses **OWL (Web Ontology Language)** to define:

    * Shape hierarchies
    * Area formulas
    * Difficulty levels
    * Geometric properties
* 🧮 **Supported Shapes**

  * Square
  * Rectangle
  * Triangle
  * Circle
  * Trapezoid
  * Parallelogram
* 🎯 **Adaptive Pedagogical Engine**

  * Randomized problem generation
  * Formula-based hints
  * Tolerance-based answer checking
  * Student performance tracking
* 🖥️ **User-Friendly GUI (Tkinter)**

  * Scrollable interface
  * Visual feedback with colors and icons
  * Keyboard support (Enter to submit)
* 📊 **Learning Progress Tracking**

  * Accuracy per shape
  * Overall performance summary
* 📚 **Ontology Transparency**

  * View ontology summaries, formulas, difficulty levels, and concept relationships

---

## 🏗️ System Architecture

```
├── OWLOntologyLoader
│   ├── Parses OWL file
│   ├── Extracts formulas
│   ├── Extracts difficulty levels
│   └── Builds shape knowledge base
│
├── GeometryOntology
│   ├── Manages shapes & concepts
│   └── Provides ontology summaries
│
├── PedagogicalEngine
│   ├── Generates problems
│   ├── Calculates correct answers
│   ├── Provides feedback & hints
│   └── Tracks learner progress
│
└── GeometryTutorGUI (Tkinter)
    ├── Interactive interface
    ├── Problem display
    ├── Answer validation
    └── Progress & ontology views
```

---

## 📂 Project Structure

```
geometry-area-tutor/
│
├── geometry_tutor.py        # Main application
├── geometry_ontology.owl    # OWL ontology (optional)
├── README.md                # Project documentation
```

> ⚠️ If `geometry_ontology.owl` is not found, the system automatically falls back to a **default built-in ontology**.

---

## 🚀 Getting Started

### 1️⃣ Requirements

* Python **3.8+**
* Standard libraries only:

  * `tkinter`
  * `math`
  * `random`
  * `xml.etree.ElementTree`
  * `os`

✅ No external dependencies required.

---

### 2️⃣ Run the Application

```bash
python geometry_tutor.py
```

---

## 🧪 Example Learning Flow

1. Select a shape (e.g., **Circle**)
2. Click **New Problem**
3. Enter the calculated area
4. Receive:

   * ✔ Correct confirmation
   * ⚠ Close attempt feedback
   * ❌ Incorrect explanation with formula-based hints
5. Track progress via **View Progress**

---

## 📖 Ontology Usage

The system uses OWL to model:

* **Classes**: Shape, Quadrilateral, Polygon, ConicSection
* **Individuals**: SquareType, CircleType, etc.
* **Properties**:

  * `hasFormula`
  * `hasDifficulty`
  * `hasDescription`
  * `hasFormulaExpression`

This enables:

* Explainable learning
* Semantic extensibility
* Academic alignment with AI & Semantic Web research

---

## 🎓 Educational Value

* Ideal for:

  * Intelligent Tutoring Systems (ITS)
  * AI in Education (AIED)
  * Semantic Web applications
  * Human–Computer Interaction (HCI)
* Suitable for:

  * Undergraduate & MSc coursework
  * Dissertation prototypes
  * Teaching demonstrations

---

## 🔮 Future Enhancements

* 🧠 Adaptive difficulty progression
* 🧾 OWL reasoning with `owlready2`
* 🎨 Shape visualization (Canvas drawings)
* 💾 Student progress persistence
* 🌐 Web-based version (Flask / Django)

---

## 👤 Author

**Peter Oduntan**
MSc Computer Science
Intelligent Tutoring Systems · Ontologies · Educational Software


