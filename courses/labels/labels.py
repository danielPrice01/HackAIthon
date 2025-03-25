# filter.py

LABELS = [
    "Introductory Programming",
    "Advanced Programming",
    "Object-Oriented Programming",
    "Functional Programming",
    "Procedural Programming",
    "Programming Paradigms",
    "Data Structures",
    "Algorithms",
    "Algorithm Analysis",
    "Computational Complexity",
    "Theory of Computation",
    "Discrete Mathematics",
    "Mathematical Foundations",
    "Proof Techniques",
    "Logic and Reasoning",
    "Software Engineering",
    "Agile Development",
    "Test-Driven Development",
    "Software Design",
    "Software Architecture",
    "Software Systems",
    "Operating Systems",
    "Computer Architecture",
    "Digital Systems",
    "Embedded Systems",
    "Systems Programming",
    "Computer Networks",
    "Distributed Systems",
    "Internet and Web Systems",
    "Cloud Computing",
    "Big Data Analytics",
    "Data Mining",
    "Data Exploration",
    "Data Visualization",
    "Database Systems",
    "NoSQL Databases",
    "SQL and Relational Databases",
    "Human–Computer Interaction",
    "User Interface Design",
    "Interaction Design",
    "Visual Design",
    "Mobile App Development",
    "iOS Programming",
    "Android Programming",
    "Web Development",
    "Frontend Development",
    "Backend Development",
    "Full-Stack Development",
    "DevOps",
    "Cybersecurity",
    "Computer and Network Security",
    "Cryptography",
    "Ethical Hacking",
    "Privacy and Security",
    "Ethical Algorithm Design",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Neural Networks",
    "Reinforcement Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Image Processing",
    "Computational Photography",
    "Robotics",
    "Computer Animation",
    "Game Design",
    "Game Development",
    "Virtual Reality",
    "Augmented Reality",
    "Interactive Graphics",
    "GPU Programming",
    "Parallel Computing",
    "Scientific Computing",
    "Numerical Methods",
    "Simulation and Modeling",
    "Quantum Computing",
    "Quantum Information Science",
    "Blockchain Technology",
    "Distributed Ledger Technology",
    "Bioinformatics",
    "Computational Biology",
    "Biomedical Image Analysis",
    "Computational Neuroscience",
    "Cognitive Science",
    "Data Science",
    "Statistical Inference",
    "Probability and Statistics",
    "Stochastic Processes",
    "Optimization Techniques",
    "DevOps Practices",
    "Research Methods",
    "Independent Study",
    "Capstone Projects",
    "Senior Thesis",
    "Special Topics",
    "Seminar Courses",
    "Interdisciplinary Studies",
    "Ethics in Technology",
    "Policy and Technology",
    "Python Programming",
    "C++ Programming",
    "Java Programming",
    "JavaScript Programming",
    "Ruby on Rails",
    "Go Programming",
    "Haskell Programming",
    "C Programming",
    "Rust Programming",
    "OCaml Programming",
    "SQL Programming",
    "R Programming",
    "MATLAB Programming",
    "TypeScript",
    "Swift Programming",
    "PHP Programming",
    "Perl Programming",
    "Recursion Techniques",
    "Iterative Methods",
    "Unit Testing",
    "Debugging Techniques",
    "Code Optimization",
    "Code Profiling",
    "Object-Oriented Design Patterns",
    "Functional Design Patterns",
    "Concurrent Programming Techniques",
    "Parallel Processing Techniques",
    "Memory Management Techniques",
    "Compiler Design Techniques",
    "Heuristic Algorithms",
    "Graph Algorithms",
    "Dynamic Programming",
    "Randomized Algorithms",
    "Machine Learning Techniques",
    "Deep Learning Techniques",
    "NLP Techniques",
    "Image Processing Techniques",
    "Simulation and Modeling Techniques"
]

label_keywords = {
    "Introductory Programming": [
        "introductory programming course", "beginner programming", "introduction to programming", "foundations of programming"
    ],
    "Advanced Programming": [
        "advanced programming", "sophisticated programming techniques", "advanced coding", "expert programming"
    ],
    "Object-Oriented Programming": [
        "object-oriented programming", "oop", "classes and objects", "inheritance", "polymorphism", "encapsulation", "object instantiation"
    ],
    "Functional Programming": [
        "functional programming", "pure functions", "immutability", "lambda calculus", "higher-order functions", "functional paradigm"
    ],
    "Procedural Programming": [
        "procedural programming", "structured programming", "step-by-step programming", "procedure-based programming"
    ],
    "Programming Paradigms": [
        "programming paradigms", "imperative paradigm", "declarative paradigm", "logic programming", "event-driven"
    ],
    "Data Structures": [
        "data structures", "arrays", "linked list", "binary tree", "heap", "graph", "stack", "queue", "hash table"
    ],
    "Algorithms": [
        "algorithm design", "sorting algorithm", "search algorithm", "recursive algorithm", "greedy algorithm"
    ],
    "Algorithm Analysis": [
        "algorithm analysis", "complexity analysis", "big o", "asymptotic analysis", "runtime analysis"
    ],
    "Computational Complexity": [
        "computational complexity", "complexity classes", "NP-hard", "NP-complete", "exponential time", "polynomial time"
    ],
    "Theory of Computation": [
        "theory of computation", "automata theory", "turing machine", "formal languages", "decidability", "computability"
    ],
    "Discrete Mathematics": [
        "discrete mathematics", "combinatorics", "graph theory", "set theory", "logic", "discrete structures"
    ],
    "Mathematical Foundations": [
        "mathematical foundations", "rigorous mathematics", "proofs", "mathematical reasoning", "theoretical foundation"
    ],
    "Proof Techniques": [
        "proof techniques", "mathematical induction", "proof by contradiction", "direct proof", "proof strategy"
    ],
    "Logic and Reasoning": [
        "deductive reasoning", "propositional logic", "predicate logic", "logical inference", "formal logic"
    ],
    "Software Engineering": [
        "software engineering", "software development lifecycle", "sdlc", "version control", "code review", "engineering practices"
    ],
    "Agile Development": [
        "agile methodology", "scrum", "kanban", "iterative development", "agile practices"
    ],
    "Test-Driven Development": [
        "test-driven development", "tdd", "unit tests first", "automated testing", "test-driven"
    ],
    "Software Design": [
        "software design", "design patterns", "architectural design", "modular design", "UML", "system design"
    ],
    "Software Architecture": [
        "software architecture", "system architecture", "architectural patterns", "microservices", "layered architecture"
    ],
    "Software Systems": [
        "software systems", "enterprise software", "system integration", "software infrastructure"
    ],
    "Operating Systems": [
        "operating system", "OS", "kernel", "process scheduling", "memory management", "file system", "multitasking"
    ],
    "Computer Architecture": [
        "computer architecture", "cpu design", "instruction set", "pipeline", "cache", "processor design", "hardware architecture"
    ],
    "Digital Systems": [
        "digital systems", "digital logic", "boolean algebra", "logic circuits", "combinational circuits", "sequential circuits"
    ],
    "Embedded Systems": [
        "embedded systems", "microcontroller", "firmware", "real-time systems", "embedded programming", "RTOS"
    ],
    "Systems Programming": [
        "systems programming", "low-level programming", "system calls", "operating system interfaces", "assembly language"
    ],
    "Computer Networks": [
        "computer networks", "network protocols", "TCP/IP", "routing", "switching", "LAN", "WAN", "network communication"
    ],
    "Distributed Systems": [
        "distributed systems", "distributed computing", "parallel systems", "consensus", "fault tolerance", "scalability"
    ],
    "Internet and Web Systems": [
        "web systems", "internet protocols", "HTTP", "REST", "client-server architecture", "HTML", "CSS", "JavaScript"
    ],
    "Cloud Computing": [
        "cloud computing", "AWS", "Azure", "Google Cloud", "virtualization", "cloud infrastructure", "cloud services"
    ],
    "Big Data Analytics": [
        "big data analytics", "big data processing", "Hadoop", "Spark", "data scalability", "massive data"
    ],
    "Data Mining": [
        "data mining", "knowledge discovery", "pattern mining", "association rules", "clustering", "outlier detection"
    ],
    "Data Exploration": [
        "exploratory data analysis", "data exploration", "EDA", "data investigation", "data profiling"
    ],
    "Data Visualization": [
        "data visualization", "visualization", "charts", "graphs", "plotting", "infographics", "data dashboards"
    ],
    "Database Systems": [
        "database systems", "DBMS", "relational databases", "data storage", "SQL", "database design"
    ],
    "NoSQL Databases": [
        "NoSQL", "non-relational", "document store", "key-value store", "MongoDB", "Cassandra", "graph databases"
    ],
    "SQL and Relational Databases": [
        "SQL", "relational databases", "structured query language", "RDBMS", "database query"
    ],
    "Human–Computer Interaction": [
        "human-computer interaction", "HCI", "user experience", "UX", "usability testing", "interaction design"
    ],
    "User Interface Design": [
        "user interface design", "UI design", "interface layout", "wireframes", "mockups", "visual interface"
    ],
    "Interaction Design": [
        "interaction design", "user interaction", "interactive design", "experience design", "interface interaction"
    ],
    "Visual Design": [
        "visual design", "graphic design", "color theory", "typography", "layout design", "visual communication"
    ],
    "Mobile App Development": [
        "mobile app development", "mobile applications", "smartphone app", "tablet app", "cross-platform mobile"
    ],
    "iOS Programming": [
        "iOS programming", "Swift", "Objective-C", "iPhone app", "iPad app", "Apple development"
    ],
    "Android Programming": [
        "Android programming", "Kotlin", "Android Studio", "Java for Android", "Android app development"
    ],
    "Web Development": [
        "web development", "website development", "web applications", "frontend", "backend", "full stack", "dynamic web"
    ],
    "Frontend Development": [
        "frontend development", "client-side", "HTML", "CSS", "JavaScript", "responsive design", "user interface"
    ],
    "Backend Development": [
        "backend development", "server-side", "APIs", "server programming", "database integration", "RESTful"
    ],
    "Full-Stack Development": [
        "full-stack development", "end-to-end web", "both frontend and backend", "complete web development"
    ],
    "DevOps": [
        "DevOps", "continuous integration", "continuous delivery", "CI/CD", "Docker", "Kubernetes", "automation", "infrastructure as code"
    ],
    "Cybersecurity": [
        "cybersecurity", "information security", "data protection", "security breaches", "vulnerability", "cyber attack"
    ],
    "Computer and Network Security": [
        "computer security", "network security", "intrusion detection", "firewall", "security protocols", "endpoint security"
    ],
    "Cryptography": [
        "cryptography", "encryption", "decryption", "public-key", "symmetric key", "cryptanalysis", "cipher"
    ],
    "Ethical Hacking": [
        "ethical hacking", "penetration testing", "vulnerability assessment", "security testing", "red teaming"
    ],
    "Privacy and Security": [
        "privacy", "data privacy", "information security", "data protection", "GDPR", "privacy laws"
    ],
    "Ethical Algorithm Design": [
        "ethical algorithm", "algorithm bias", "fairness", "transparency", "accountability", "ethical design", "algorithm ethics"
    ],
    "Artificial Intelligence": [
        "artificial intelligence", " AI ", "intelligent systems", "machine intelligence", "autonomous systems"
    ],
    "Machine Learning": [
        "machine learning", "ML", "supervised learning", "unsupervised learning", "predictive modeling", "classification", "regression"
    ],
    "Deep Learning": [
        "deep learning", "deep neural networks", "convolutional neural network", "recurrent neural network", "deep architecture"
    ],
    "Neural Networks": [
        "neural network", "artificial neural network", "ANN", "backpropagation", "feedforward network"
    ],
    "Reinforcement Learning": [
        "reinforcement learning", "RL", "reward-based learning", "q-learning", "policy gradient", "agent learning"
    ],
    "Natural Language Processing": [
        "natural language processing", "NLP", "text processing", "language model", "sentiment analysis", "tokenization", "parsing text"
    ],
    "Computer Vision": [
        "computer vision", "image recognition", "object detection", "visual analysis", "scene understanding", "feature extraction in images"
    ],
    "Image Processing": [
        "image processing", "image filtering", "edge detection", "segmentation", "morphological operations", "image enhancement"
    ],
    "Computational Photography": [
        "computational photography", "photo processing", "HDR", "panorama", "photo stitching", "image compositing"
    ],
    "Robotics": [
        "robotics", "robot", "automation", "control systems", "robot programming", "mechanical systems", "autonomous robots"
    ],
    "Computer Animation": [
        "computer animation", "animation", "3D animation", "motion capture", "keyframe animation", "animated graphics"
    ],
    "Game Design": [
        "game design", "game mechanics", "level design", "gameplay", "interactive design", "game theory", "design document"
    ],
    "Game Development": [
        "game development", "game programming", "game engine", "Unity", "Unreal Engine", "interactive entertainment"
    ],
    "Virtual Reality": [
        "virtual reality", " VR ", "immersive experience", "vr headset", "simulated reality", "virtual environment"
    ],
    "Augmented Reality": [
        "augmented reality", " AR ", "mixed reality", "overlay", "real-time augmentation", "AR application"
    ],
    "Interactive Graphics": [
        "interactive graphics", "interactive visualization", "graphics programming", "user interaction graphics", "real-time graphics"
    ],
    "GPU Programming": [
        "GPU programming", "CUDA", "GPGPU", "graphics processing unit", "parallel GPU", "NVIDIA CUDA"
    ],
    "Parallel Computing": [
        "parallel computing", "parallel processing", "multithreading", "concurrency", "SIMD", "MIMD", "parallel algorithms"
    ],
    "Scientific Computing": [
        "scientific computing", "numerical computing", "computational science", "engineering simulation", "scientific simulation"
    ],
    "Numerical Methods": [
        "numerical methods", "numerical analysis", "finite difference", "iterative methods", "solver", "approximation method"
    ],
    "Simulation and Modeling": [
        "simulation", "modeling", "computer simulation", "system modeling", "virtual modeling", "simulation techniques"
    ],
    "Quantum Computing": [
        "quantum computing", "quantum algorithm", "qubit", "superposition", "entanglement", "quantum circuit"
    ],
    "Quantum Information Science": [
        "quantum information", "quantum communication", "quantum cryptography", "quantum channel", "quantum data"
    ],
    "Blockchain Technology": [
        "blockchain", "distributed ledger", "cryptocurrency", "bitcoin", "smart contracts", "blockchain protocol"
    ],
    "Distributed Ledger Technology": [
        "distributed ledger", "DLT", "decentralized ledger", "blockchain ledger", "ledger technology"
    ],
    "Bioinformatics": [
        "bioinformatics", "genomics", "sequence analysis", "biological data", "protein structure", "DNA analysis", "RNA analysis"
    ],
    "Computational Biology": [
        "computational biology", "biological computation", "biological modeling", "systems biology", "computational genomics"
    ],
    "Biomedical Image Analysis": [
        "biomedical image analysis", "medical imaging", "MRI", "CT scan", "ultrasound", "diagnostic imaging", "medical image processing"
    ],
    "Computational Neuroscience": [
        "computational neuroscience", "neural modeling", "brain simulation", "neurocomputing", "neuroscience modeling"
    ],
    "Cognitive Science": [
        "cognitive science", "cognition", "brain", "perception", "psychology", "human mind", "cognitive processes"
    ],
    "Data Science": [
        "data science", "data analysis", "predictive analytics", "data mining", "statistical modeling", "big data"
    ],
    "Statistical Inference": [
        "statistical inference", "hypothesis testing", "confidence interval", "p-value", "inferential statistics"
    ],
    "Probability and Statistics": [
        "probability", "statistics", "statistical methods", "random variables", "data distribution", "statistical analysis"
    ],
    "Stochastic Processes": [
        "stochastic process", "random process", "markov", "poisson", "stochastic modeling", "random process theory"
    ],
    "Optimization Techniques": [
        "optimization", "optimization algorithms", "linear programming", "gradient descent", "convex optimization", "optimization method"
    ],
    "DevOps Practices": [
        "devops practices", "continuous integration", "continuous delivery", "CI/CD", "automation", "infrastructure as code"
    ],
    "Research Methods": [
        "research methods", "experimental design", "research methodology", "data collection", "analysis techniques", "study design"
    ],
    "Independent Study": [
        "independent study", "self-directed research", "independent project", "custom research", "individual study"
    ],
    "Capstone Projects": [
        "capstone project", "senior project", "final project", "culminating project", "capstone experience"
    ],
    "Senior Thesis": [
        "senior thesis", "thesis project", "final thesis", "research thesis", "capstone thesis"
    ],
    "Special Topics": [
        "special topics", "variable topics", "current research topics", "emerging topics", "topic-specific"
    ],
    "Seminar Courses": [
        "seminar", "discussion course", "colloquium", "graduate seminar", "seminar-style"
    ],
    "Interdisciplinary Studies": [
        "interdisciplinary", "cross-disciplinary", "multidisciplinary", "integrative studies", "combined disciplines"
    ],
    "Ethics in Technology": [
        "ethics in technology", "ethical issues", "technology ethics", "moral implications", "responsible computing", "tech ethics"
    ],
    "Policy and Technology": [
        "technology policy", "regulation", "government policy", "tech law", "data policy", "regulatory"
    ],
    "Python Programming": [
        "python programming", "python 3", "python code", "python script", "python language"
    ],
    "C++ Programming": [
        "c++ programming", "cplusplus", "c plus plus", "cpp", "c++ language"
    ],
    "Java Programming": [
        "java programming", "java code", "jdk", "jre", "java language"
    ],
    "JavaScript Programming": [
        "javascript programming", "js", "node.js", "react", "angular", "vue.js", "javascript language"
    ],
    "Ruby on Rails": [
        "ruby on rails", "rails", "ror", "ruby web framework", "ruby on rails framework"
    ],
    "Go Programming": [
        "go programming", "golang", "go language", "go-lang", "golang development"
    ],
    "Haskell Programming": [
        "haskell programming", "haskell", "functional programming in haskell", "haskell language"
    ],
    "C Programming": [
        " c programming", " c language", "ansi c ", " c code"
    ],
    "Rust Programming": [
        "rust programming", "rust language", "rust-lang", "rust code"
    ],
    "OCaml Programming": [
        "ocaml programming", "ocaml", "ocaml language"
    ],
    "SQL Programming": [
        "sql programming", "sql query", "structured query language", "sql language"
    ],
    "R Programming": [
        " r programming", " r language", " r stats", " r analysis", " r coding"
    ],
    "MATLAB Programming": [
        "matlab programming", "matlab", "matrix laboratory", "numerical computing matlab", "matlab code"
    ],
    "TypeScript": [
        "typescript programming", "typescript", " ts language", "typescript code"
    ],
    "Swift Programming": [
        "swift programming", "swift language", "ios swift", "swift code"
    ],
    "PHP Programming": [
        "php programming", "php", "php script", "php code"
    ],
    "Perl Programming": [
        "perl programming", "perl script", "perl language", "perl code"
    ],
    "Recursion Techniques": [
        "recursion", "recursive function", "recursive technique", "recursive algorithm"
    ],
    "Iterative Methods": [
        "iterative methods", "iteration", "looping algorithm", "iterative process", "for loop", "while loop"
    ],
    "Unit Testing": [
        "unit testing", "test-driven", "tdd", "test case", "unit test", "automated test"
    ],
    "Debugging Techniques": [
        "debugging", "debug", "troubleshooting", "error tracing", "bug fixing"
    ],
    "Code Optimization": [
        "code optimization", "optimize", "performance optimization", "efficient code", "optimization technique"
    ],
    "Code Profiling": [
        "code profiling", "profiling", "performance profiling", "benchmarking", "runtime analysis"
    ],
    "Object-Oriented Design Patterns": [
        "object-oriented design patterns", "design patterns", "singleton", "factory", "observer", "strategy", "mvc"
    ],
    "Functional Design Patterns": [
        "functional design patterns", "functional patterns", "higher-order function pattern", "functional composition"
    ],
    "Concurrent Programming Techniques": [
        "concurrent programming", "multithreading", "concurrency", "parallel execution", "synchronization", "thread safety"
    ],
    "Parallel Processing Techniques": [
        "parallel processing", "data parallel", "task parallel", "SIMD", "MIMD", "parallel algorithms"
    ],
    "Memory Management Techniques": [
        "memory management", "garbage collection", "manual memory", "allocation", "deallocation", "memory leak"
    ],
    "Compiler Design Techniques": [
        "compiler design", "parsing", "syntax analysis", "code generation", "compiler construction", "compiler optimization"
    ],
    "Heuristic Algorithms": [
        "heuristic algorithm", "heuristics", "approximation algorithm", "rule-of-thumb", "greedy heuristic"
    ],
    "Graph Algorithms": [
        "graph algorithm", "graph traversal", "dijkstra", "a star", "minimum spanning tree", "graph search"
    ],
    "Dynamic Programming": [
        "dynamic programming", "DP", "recursive optimization", "memoization", "optimal substructure"
    ],
    "Randomized Algorithms": [
        "randomized algorithm", "randomization", "monte carlo", "probabilistic algorithm", "random sampling"
    ],
    "Machine Learning Techniques": [
        "machine learning technique", "feature extraction", "model training", "supervised learning technique", "training algorithm"
    ],
    "Deep Learning Techniques": [
        "deep learning technique", "convolutional neural network", "recurrent neural network", "deep learning model", "neural network training"
    ],
    "NLP Techniques": [
        "NLP technique", "natural language processing technique", "tokenization", "stemming", "lemmatization", "stopword removal"
    ],
    "Image Processing Techniques": [
        "image processing technique", "image filtering", "edge detection", "segmentation", "morphological operations", "image enhancement"
    ],
    "Simulation and Modeling Techniques": [
        "simulation technique", "modeling technique", "computer simulation", "system modeling", "virtual modeling", "simulation method"
    ]
}
