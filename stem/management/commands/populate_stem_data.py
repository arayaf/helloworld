from django.core.management.base import BaseCommand
from stem.models import Subject, Topic, Lesson, Quiz, QuizOption, Formula


class Command(BaseCommand):
    help = 'Populate the database with initial STEM content'

    def handle(self, *args, **options):
        self.stdout.write('Creating STEM subjects and content...')
        
        # Create Mathematics Subject
        math_subject, created = Subject.objects.get_or_create(
            name='Mathematics',
            defaults={
                'description': 'Fundamental mathematical concepts for engineering students',
                'icon': 'fas fa-calculator',
                'color': '#DC143C'
            }
        )
        
        # Create Physics Subject
        physics_subject, created = Subject.objects.get_or_create(
            name='Physics',
            defaults={
                'description': 'Core physics principles and applications in engineering',
                'icon': 'fas fa-atom',
                'color': '#DC143C'
            }
        )
        
        # Create Chemistry Subject
        chemistry_subject, created = Subject.objects.get_or_create(
            name='Chemistry',
            defaults={
                'description': 'Essential chemistry concepts for engineering applications',
                'icon': 'fas fa-flask',
                'color': '#DC143C'
            }
        )
        
        # Create Computer Science Subject
        cs_subject, created = Subject.objects.get_or_create(
            name='Computer Science',
            defaults={
                'description': 'Programming fundamentals and computer science concepts',
                'icon': 'fas fa-laptop-code',
                'color': '#DC143C'
            }
        )
        
        # Create Mathematics Topics
        calculus_topic, created = Topic.objects.get_or_create(
            subject=math_subject,
            title='Calculus Fundamentals',
            defaults={
                'description': 'Introduction to differential and integral calculus',
                'difficulty_level': 2,
                'estimated_duration': 120,
                'order': 1
            }
        )
        
        algebra_topic, created = Topic.objects.get_or_create(
            subject=math_subject,
            title='Linear Algebra',
            defaults={
                'description': 'Vectors, matrices, and linear transformations',
                'difficulty_level': 2,
                'estimated_duration': 90,
                'order': 2
            }
        )
        
        # Create Physics Topics
        mechanics_topic, created = Topic.objects.get_or_create(
            subject=physics_subject,
            title='Classical Mechanics',
            defaults={
                'description': 'Newton\'s laws, motion, and forces',
                'difficulty_level': 2,
                'estimated_duration': 100,
                'order': 1
            }
        )
        
        # Create Mathematics Lessons
        calc_lesson1, created = Lesson.objects.get_or_create(
            topic=calculus_topic,
            title='Introduction to Limits',
            defaults={
                'content': '''
                <h3>What are Limits?</h3>
                <p>A limit describes the behavior of a function as its input approaches a particular value. 
                It's fundamental to understanding calculus.</p>
                
                <h4>Definition</h4>
                <p>The limit of f(x) as x approaches a is L, written as:</p>
                <p><strong>lim(x→a) f(x) = L</strong></p>
                
                <h4>Key Concepts</h4>
                <ul>
                    <li>Limits can exist even when the function is not defined at that point</li>
                    <li>Left-hand and right-hand limits must be equal for the limit to exist</li>
                    <li>Limits help us understand continuity and differentiability</li>
                </ul>
                
                <h4>Example</h4>
                <p>Consider f(x) = (x² - 1)/(x - 1)</p>
                <p>Even though f(1) is undefined, lim(x→1) f(x) = 2</p>
                ''',
                'lesson_type': 'theory',
                'order': 1
            }
        )
        
        calc_lesson2, created = Lesson.objects.get_or_create(
            topic=calculus_topic,
            title='Derivatives',
            defaults={
                'content': '''
                <h3>Understanding Derivatives</h3>
                <p>The derivative represents the rate of change of a function at any given point.</p>
                
                <h4>Definition</h4>
                <p>f'(x) = lim(h→0) [f(x+h) - f(x)]/h</p>
                
                <h4>Common Derivative Rules</h4>
                <ul>
                    <li>Power Rule: d/dx(xⁿ) = nxⁿ⁻¹</li>
                    <li>Product Rule: d/dx(fg) = f'g + fg'</li>
                    <li>Chain Rule: d/dx(f(g(x))) = f'(g(x)) · g'(x)</li>
                </ul>
                
                <h4>Applications</h4>
                <p>Derivatives are used to find:</p>
                <ul>
                    <li>Velocity and acceleration</li>
                    <li>Maximum and minimum values</li>
                    <li>Slopes of tangent lines</li>
                </ul>
                ''',
                'lesson_type': 'theory',
                'order': 2
            }
        )
        
        # Create Physics Lessons
        mechanics_lesson1, created = Lesson.objects.get_or_create(
            topic=mechanics_topic,
            title='Newton\'s Laws of Motion',
            defaults={
                'content': '''
                <h3>Newton's Three Laws</h3>
                
                <h4>First Law (Law of Inertia)</h4>
                <p>An object at rest stays at rest, and an object in motion stays in motion 
                with constant velocity, unless acted upon by an external force.</p>
                
                <h4>Second Law</h4>
                <p>F = ma</p>
                <p>The acceleration of an object is directly proportional to the net force 
                and inversely proportional to its mass.</p>
                
                <h4>Third Law (Action-Reaction)</h4>
                <p>For every action, there is an equal and opposite reaction.</p>
                
                <h4>Applications in Engineering</h4>
                <ul>
                    <li>Structural analysis</li>
                    <li>Mechanical design</li>
                    <li>Vehicle dynamics</li>
                </ul>
                ''',
                'lesson_type': 'theory',
                'order': 1
            }
        )
        
        # Create Quizzes
        calc_quiz1, created = Quiz.objects.get_or_create(
            lesson=calc_lesson1,
            question='What is the limit of f(x) = x² as x approaches 3?',
            defaults={
                'question_type': 'multiple_choice',
                'points': 1,
                'explanation': 'The limit of x² as x approaches 3 is simply 3² = 9.'
            }
        )
        
        if created:
            QuizOption.objects.create(quiz=calc_quiz1, option_text='6', is_correct=False, order=1)
            QuizOption.objects.create(quiz=calc_quiz1, option_text='9', is_correct=True, order=2)
            QuizOption.objects.create(quiz=calc_quiz1, option_text='3', is_correct=False, order=3)
            QuizOption.objects.create(quiz=calc_quiz1, option_text='27', is_correct=False, order=4)
        
        physics_quiz1, created = Quiz.objects.get_or_create(
            lesson=mechanics_lesson1,
            question='According to Newton\'s second law, if you double the force applied to an object, what happens to its acceleration?',
            defaults={
                'question_type': 'multiple_choice',
                'points': 1,
                'explanation': 'Since F = ma, if force doubles and mass stays the same, acceleration also doubles.'
            }
        )
        
        if created:
            QuizOption.objects.create(quiz=physics_quiz1, option_text='It doubles', is_correct=True, order=1)
            QuizOption.objects.create(quiz=physics_quiz1, option_text='It halves', is_correct=False, order=2)
            QuizOption.objects.create(quiz=physics_quiz1, option_text='It stays the same', is_correct=False, order=3)
            QuizOption.objects.create(quiz=physics_quiz1, option_text='It quadruples', is_correct=False, order=4)
        
        # Create Formulas
        derivative_formula, created = Formula.objects.get_or_create(
            subject=math_subject,
            name='Power Rule for Derivatives',
            defaults={
                'formula_text': 'd/dx(xⁿ) = nxⁿ⁻¹',
                'description': 'The derivative of x raised to the power n',
                'variables': {
                    'x': 'The variable',
                    'n': 'The exponent (constant)'
                },
                'example_usage': 'd/dx(x³) = 3x²'
            }
        )
        
        newton_formula, created = Formula.objects.get_or_create(
            subject=physics_subject,
            name='Newton\'s Second Law',
            defaults={
                'formula_text': 'F = ma',
                'description': 'Force equals mass times acceleration',
                'variables': {
                    'F': 'Force (Newtons)',
                    'm': 'Mass (kg)',
                    'a': 'Acceleration (m/s²)'
                },
                'example_usage': 'If m = 5 kg and a = 2 m/s², then F = 5 × 2 = 10 N'
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created STEM content!')
        )