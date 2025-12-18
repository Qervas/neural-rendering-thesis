from manim import *

class NeRFRayMarching(Scene):
    def construct(self):
        # Colors
        BLUE = "#00b3e7"
        TURQUOISE = "#0cc7d3"
        RED = "#ff6b6b"

        # Title
        title = Text("NeRF: Ray Marching", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Camera
        step1 = Text("Step 1: Camera looks through one pixel", font_size=28, color=WHITE)
        step1.to_edge(DOWN, buff=0.8)

        # Camera body
        camera_body = RoundedRectangle(
            width=1.2, height=0.9, corner_radius=0.1,
            fill_color=GRAY_D, fill_opacity=1, stroke_color=WHITE
        )
        camera_lens = Circle(radius=0.25, fill_color=BLUE, fill_opacity=1, stroke_color=WHITE)
        camera = VGroup(camera_body, camera_lens)
        camera.move_to(LEFT * 5.5 + DOWN * 0.5)
        camera_label = Text("Camera", font_size=20, color=GRAY_B)
        camera_label.next_to(camera, DOWN, buff=0.2)

        self.play(Write(step1))
        self.play(FadeIn(camera), Write(camera_label))

        # Image plane (pixel grid)
        pixel_grid = VGroup()
        for i in range(4):
            for j in range(3):
                rect = Rectangle(width=0.3, height=0.3, stroke_color=GRAY, stroke_width=1)
                rect.move_to(LEFT * 4 + DOWN * 0.5 + RIGHT * j * 0.3 + UP * i * 0.3 - UP * 0.45)
                pixel_grid.add(rect)

        # Highlight one pixel
        highlight_pixel = Rectangle(
            width=0.3, height=0.3,
            fill_color=BLUE, fill_opacity=0.4,
            stroke_color=BLUE, stroke_width=2
        )
        highlight_pixel.move_to(LEFT * 4 + DOWN * 0.5 + RIGHT * 0.3)

        pixel_label = Text("Image", font_size=18, color=GRAY_B)
        pixel_label.next_to(pixel_grid, DOWN, buff=0.2)

        self.play(FadeIn(pixel_grid), Write(pixel_label))
        self.play(FadeIn(highlight_pixel))
        self.wait(0.5)

        # Step 2: Shoot ray
        self.play(FadeOut(step1))
        step2 = Text("Step 2: Shoot a ray into the scene", font_size=28, color=WHITE)
        step2.to_edge(DOWN, buff=0.8)
        self.play(Write(step2))

        # 3D Scene (ellipse)
        scene_ellipse = Ellipse(width=2.5, height=1.8, fill_color=GRAY_E, fill_opacity=0.5, stroke_color=GRAY)
        scene_ellipse.move_to(RIGHT * 2 + DOWN * 0.5)
        scene_label = Text("3D Scene", font_size=18, color=GRAY_B)
        scene_label.move_to(scene_ellipse.get_center())

        self.play(FadeIn(scene_ellipse), Write(scene_label))

        # Ray
        ray_start = highlight_pixel.get_center()
        ray_end = RIGHT * 4.5 + DOWN * 0.5
        ray = DashedLine(ray_start, ray_end, color=BLUE, dash_length=0.15, stroke_width=4)

        self.play(Create(ray), run_time=1.5)
        self.wait(0.5)

        # Step 3: Sample points
        self.play(FadeOut(step2))
        step3 = Text("Step 3: Sample points along the ray", font_size=28, color=WHITE)
        step3.to_edge(DOWN, buff=0.8)
        self.play(Write(step3))

        # Sample points
        sample_points = VGroup()
        sample_labels = VGroup()
        positions = [LEFT * 2.5, LEFT * 1, RIGHT * 0.5, RIGHT * 2]

        for i, pos in enumerate(positions):
            point = Circle(radius=0.2, fill_color=RED, fill_opacity=0.9 - i*0.15, stroke_color=WHITE, stroke_width=2)
            point.move_to(pos + DOWN * 0.5)
            label = Text(str(i+1), font_size=16, color=WHITE)
            label.move_to(point.get_center())
            sample_points.add(point)
            sample_labels.add(label)

        for point, label in zip(sample_points, sample_labels):
            self.play(
                GrowFromCenter(point),
                FadeIn(label),
                run_time=0.4
            )
        self.wait(0.5)

        # Step 4: Query neural network
        self.play(FadeOut(step3))
        step4 = Text("Step 4: Ask neural network - \"What color? How dense?\"", font_size=28, color=WHITE)
        step4.to_edge(DOWN, buff=0.8)
        self.play(Write(step4))

        # Neural network box
        nn_box = RoundedRectangle(
            width=3, height=1.2, corner_radius=0.15,
            fill_color="#1a1a2e", fill_opacity=0.9,
            stroke_color=BLUE, stroke_width=2
        )
        nn_box.move_to(UP * 2)
        nn_title = Text("Neural Network", font_size=20, color=BLUE)
        nn_subtitle = Text("(x,y,z) + direction → color + density", font_size=14, color=GRAY_B)
        nn_title.move_to(nn_box.get_center() + UP * 0.25)
        nn_subtitle.move_to(nn_box.get_center() + DOWN * 0.25)

        self.play(FadeIn(nn_box), Write(nn_title), Write(nn_subtitle))

        # Arrows from points to network
        arrows = VGroup()
        for point in sample_points:
            arrow = Arrow(
                point.get_top(),
                nn_box.get_bottom(),
                color=TURQUOISE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )
            arrows.add(arrow)

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2), run_time=1.5)

        # Query animation
        for i, point in enumerate(sample_points):
            self.play(
                point.animate.set_fill(YELLOW, opacity=0.9),
                run_time=0.2
            )
            self.play(
                point.animate.set_fill(RED, opacity=0.9 - i*0.15),
                run_time=0.2
            )

        self.wait(0.5)

        # Step 5: Blend to final pixel
        self.play(FadeOut(step4), FadeOut(arrows))
        step5 = Text("Step 5: Blend colors → Final pixel!", font_size=28, color=WHITE)
        step5.to_edge(DOWN, buff=0.8)
        self.play(Write(step5))

        # Output pixel
        output_pixel = Square(side_length=0.8, fill_color=RED, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
        output_pixel.move_to(RIGHT * 5.5 + DOWN * 0.5)
        output_label = Text("Final\ncolor", font_size=16, color=GRAY_B)
        output_label.next_to(output_pixel, DOWN, buff=0.2)

        # Arrow to output
        blend_arrow = Arrow(RIGHT * 3.5 + DOWN * 0.5, output_pixel.get_left(), color=BLUE, stroke_width=3)

        self.play(Create(blend_arrow))

        # Animate blending
        self.play(
            *[point.animate.scale(0.5).set_opacity(0.3) for point in sample_points],
            GrowFromCenter(output_pixel),
            Write(output_label),
            run_time=1.5
        )

        # Final note
        self.play(FadeOut(step5))
        final_note = Text("Repeat for every pixel in the image!", font_size=24, color=TURQUOISE)
        final_note.to_edge(DOWN, buff=0.8)
        self.play(Write(final_note))

        self.wait(2)


class GaussianSplatting(Scene):
    def construct(self):
        # Colors
        BLUE = "#00b3e7"
        TURQUOISE = "#0cc7d3"

        # Title
        title = Text("3D Gaussian Splatting", font_size=48, color=TURQUOISE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Step 1: Show 3D Gaussians
        step1 = Text("Step 1: Scene = Millions of fuzzy colored blobs", font_size=28, color=WHITE)
        step1.to_edge(DOWN, buff=0.8)
        self.play(Write(step1))

        # 3D space box
        box = Cube(side_length=3, fill_opacity=0.1, stroke_color=GRAY, stroke_width=1)
        box.move_to(LEFT * 3)
        self.play(Create(box))

        # Gaussians (ellipses with gradient)
        gaussians = VGroup()
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        positions = [
            LEFT * 3.5 + UP * 0.5,
            LEFT * 2.5 + DOWN * 0.3,
            LEFT * 3 + UP * 0.2 + OUT * 0.5,
            LEFT * 3.8 + DOWN * 0.5,
            LEFT * 2.8 + UP * 0.8,
            LEFT * 3.2 + DOWN * 0.1,
        ]

        for i, (pos, color) in enumerate(zip(positions, colors)):
            gauss = Ellipse(
                width=0.8 + np.random.rand() * 0.4,
                height=0.5 + np.random.rand() * 0.3,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=0
            )
            # Convert to proper 3D point for move_to
            gauss.move_to(np.array([pos[0], pos[1], 0]))
            gauss.rotate(np.random.rand() * PI / 4)
            gaussians.add(gauss)

        self.play(LaggedStart(*[GrowFromCenter(g) for g in gaussians], lag_ratio=0.15))

        label_3d = Text("3D Space", font_size=20, color=GRAY_B)
        label_3d.next_to(box, DOWN)
        self.play(Write(label_3d))
        self.wait(0.5)

        # Step 2: Project
        self.play(FadeOut(step1))
        step2 = Text("Step 2: Project onto screen (GPU rasterization)", font_size=28, color=WHITE)
        step2.to_edge(DOWN, buff=0.8)
        self.play(Write(step2))

        # Arrow
        project_arrow = Arrow(LEFT * 1, RIGHT * 1, color=BLUE, stroke_width=4)
        project_text = Text("Project", font_size=20, color=BLUE)
        project_text.next_to(project_arrow, UP)
        self.play(Create(project_arrow), Write(project_text))

        # 2D Image
        image_frame = Rectangle(width=3, height=2.2, stroke_color=WHITE, stroke_width=2)
        image_frame.move_to(RIGHT * 3.5)
        self.play(Create(image_frame))

        # Project gaussians
        projected = VGroup()
        for i, (g, color) in enumerate(zip(gaussians, colors)):
            proj = Ellipse(
                width=g.width * 0.9,
                height=g.height * 0.9,
                fill_color=color,
                fill_opacity=0.6,
                stroke_width=0
            )
            # Map to image position
            new_x = 3.5 + (g.get_center()[0] + 3) * 0.4
            new_y = g.get_center()[1] * 0.6
            proj.move_to(np.array([new_x, new_y, 0]))
            projected.add(proj)

        self.play(
            *[TransformFromCopy(g, p) for g, p in zip(gaussians, projected)],
            run_time=1.5
        )

        label_2d = Text("2D Image", font_size=20, color=GRAY_B)
        label_2d.next_to(image_frame, DOWN)
        self.play(Write(label_2d))
        self.wait(0.5)

        # Speed badge
        self.play(FadeOut(step2))
        step3 = Text("Result: Real-time rendering!", font_size=28, color=WHITE)
        step3.to_edge(DOWN, buff=0.8)

        speed_badge = RoundedRectangle(
            width=2.5, height=0.8, corner_radius=0.3,
            fill_color=TURQUOISE, fill_opacity=1,
            stroke_width=0
        )
        speed_badge.next_to(image_frame, UP, buff=0.3)
        speed_text = Text("30+ FPS!", font_size=24, color=WHITE, weight=BOLD)
        speed_text.move_to(speed_badge)

        self.play(Write(step3))
        self.play(GrowFromCenter(speed_badge), Write(speed_text))

        self.wait(2)


class NeRFTraining(Scene):
    """Explains how NeRF's neural network learns from photos"""
    def construct(self):
        BLUE = "#00b3e7"
        TURQUOISE = "#0cc7d3"
        RED = "#ff6b6b"

        # Title
        title = Text("How NeRF Learns", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Step 1: Show training photos
        step1 = Text("Step 1: Start with photos from different angles", font_size=26, color=WHITE)
        step1.to_edge(DOWN, buff=0.8)
        self.play(Write(step1))

        # Create multiple photo frames around a center object
        photos = VGroup()
        photo_positions = [
            LEFT * 4 + UP * 1,
            LEFT * 4 + DOWN * 1,
            LEFT * 2 + UP * 1.5,
            LEFT * 2 + DOWN * 1.5,
        ]

        for i, pos in enumerate(photo_positions):
            photo = Rectangle(width=1.2, height=0.9, fill_color=GRAY_D, fill_opacity=0.8, stroke_color=WHITE)
            photo.move_to(pos)
            # Add a simple icon inside
            icon = Square(side_length=0.3, fill_color=BLUE, fill_opacity=0.7, stroke_width=0)
            icon.move_to(pos)
            photos.add(VGroup(photo, icon))

        self.play(LaggedStart(*[FadeIn(p) for p in photos], lag_ratio=0.2))

        photos_label = Text("Training Photos", font_size=18, color=GRAY_B)
        photos_label.move_to(LEFT * 3 + DOWN * 2.5)
        self.play(Write(photos_label))
        self.wait(0.5)

        # Step 2: Neural network (empty at first)
        self.play(FadeOut(step1))
        step2 = Text("Step 2: Neural network starts with random weights", font_size=26, color=WHITE)
        step2.to_edge(DOWN, buff=0.8)
        self.play(Write(step2))

        # Neural network diagram
        nn_box = RoundedRectangle(
            width=3.5, height=2, corner_radius=0.15,
            fill_color="#1a1a2e", fill_opacity=0.9,
            stroke_color=BLUE, stroke_width=2
        )
        nn_box.move_to(RIGHT * 0.5)

        nn_title = Text("Neural Network", font_size=20, color=BLUE)
        nn_title.move_to(nn_box.get_top() + DOWN * 0.4)

        # Input/output labels
        input_text = Text("(x,y,z,θ,φ)", font_size=16, color=GRAY_B)
        input_text.move_to(nn_box.get_center() + UP * 0.2)
        output_text = Text("→ (R,G,B,σ)", font_size=16, color=GRAY_B)
        output_text.move_to(nn_box.get_center() + DOWN * 0.3)

        random_label = Text("???", font_size=32, color=RED)
        random_label.move_to(nn_box.get_center() + DOWN * 0.8)

        self.play(FadeIn(nn_box), Write(nn_title))
        self.play(Write(input_text), Write(output_text), Write(random_label))
        self.wait(0.5)

        # Step 3: Training loop
        self.play(FadeOut(step2), FadeOut(random_label))
        step3 = Text("Step 3: Training loop - render, compare, adjust", font_size=26, color=WHITE)
        step3.to_edge(DOWN, buff=0.8)
        self.play(Write(step3))

        # Show rendered vs real comparison
        rendered_frame = Rectangle(width=1.4, height=1.0, stroke_color=TURQUOISE, stroke_width=2)
        rendered_frame.move_to(RIGHT * 4 + UP * 0.8)
        rendered_label = Text("NeRF renders", font_size=14, color=TURQUOISE)
        rendered_label.next_to(rendered_frame, UP, buff=0.15)

        real_frame = Rectangle(width=1.4, height=1.0, stroke_color=GREEN, stroke_width=2)
        real_frame.move_to(RIGHT * 4 + DOWN * 0.8)
        real_label = Text("Real photo", font_size=14, color=GREEN)
        real_label.next_to(real_frame, DOWN, buff=0.15)

        # Arrow from network to rendered
        render_arrow = Arrow(nn_box.get_right(), rendered_frame.get_left(), color=TURQUOISE, stroke_width=2)

        self.play(Create(render_arrow), FadeIn(rendered_frame), Write(rendered_label))
        self.play(FadeIn(real_frame), Write(real_label))

        # Compare arrow
        compare_arrow = DoubleArrow(
            rendered_frame.get_bottom() + DOWN * 0.1,
            real_frame.get_top() + UP * 0.1,
            color=RED, stroke_width=3
        )
        compare_text = Text("Loss", font_size=16, color=RED)
        compare_text.next_to(compare_arrow, RIGHT, buff=0.1)

        self.play(Create(compare_arrow), Write(compare_text))
        self.wait(0.3)

        # Backprop arrow
        backprop_arrow = CurvedArrow(
            compare_arrow.get_center() + LEFT * 0.5,
            nn_box.get_right() + DOWN * 0.5,
            color=YELLOW, angle=-PI/4
        )
        backprop_text = Text("Adjust weights", font_size=14, color=YELLOW)
        backprop_text.next_to(backprop_arrow, DOWN, buff=0.1)

        self.play(Create(backprop_arrow), Write(backprop_text))
        self.wait(0.5)

        # Step 4: Show improvement
        self.play(FadeOut(step3))
        step4 = Text("Repeat thousands of times → Network learns the scene!", font_size=26, color=WHITE)
        step4.to_edge(DOWN, buff=0.8)
        self.play(Write(step4))

        # Animate improvement
        for _ in range(3):
            self.play(
                nn_box.animate.set_stroke(TURQUOISE, width=3),
                compare_arrow.animate.set_color(YELLOW),
                run_time=0.3
            )
            self.play(
                nn_box.animate.set_stroke(BLUE, width=2),
                compare_arrow.animate.set_color(RED),
                run_time=0.3
            )

        # Final state - network "learned"
        learned_label = Text("Learned!", font_size=24, color=GREEN)
        learned_label.move_to(nn_box.get_center())

        self.play(
            FadeOut(compare_arrow), FadeOut(compare_text),
            FadeOut(backprop_arrow), FadeOut(backprop_text),
            Write(learned_label)
        )

        # Success badge
        success = Text("✓ Can render any viewpoint!", font_size=22, color=GREEN)
        success.move_to(RIGHT * 4)
        self.play(Write(success))

        self.wait(2)


class GaussianSplattingTraining(Scene):
    """Explains how 3D Gaussians are optimized during training - CLEAR VERSION"""
    def construct(self):
        BLUE = "#00b3e7"
        TURQUOISE = "#0cc7d3"
        RED = "#ff6b6b"

        # Title
        title = Text("How 3D Gaussian Splatting Learns", font_size=44, color=TURQUOISE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.3)

        # ============ PART 1: What is a Gaussian? ============
        step1 = Text("First: What IS a Gaussian?", font_size=28, color=WHITE)
        step1.to_edge(DOWN, buff=0.8)
        self.play(Write(step1))

        # Show ONE Gaussian with its properties
        demo_gauss = Ellipse(
            width=2, height=1.2,
            fill_color=RED, fill_opacity=0.6,
            stroke_color=WHITE, stroke_width=2
        )
        demo_gauss.move_to(LEFT * 2)

        self.play(GrowFromCenter(demo_gauss))

        # Label its properties with arrows
        props_title = Text("Each Gaussian has:", font_size=20, color=GRAY_B)
        props_title.move_to(RIGHT * 2.5 + UP * 1.5)

        prop1 = Text("• Position (x, y, z)", font_size=18, color=WHITE)
        prop2 = Text("• Shape (round or stretched)", font_size=18, color=WHITE)
        prop3 = Text("• Color (RGB)", font_size=18, color=WHITE)
        prop4 = Text("• Opacity (transparent → solid)", font_size=18, color=WHITE)

        props = VGroup(prop1, prop2, prop3, prop4)
        props.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        props.move_to(RIGHT * 2.5 + DOWN * 0.3)

        self.play(Write(props_title))
        for p in props:
            self.play(Write(p), run_time=0.4)

        # Animate the properties
        self.play(demo_gauss.animate.move_to(LEFT * 3), run_time=0.5)  # position
        self.play(demo_gauss.animate.move_to(LEFT * 2), run_time=0.5)
        self.play(demo_gauss.animate.stretch(1.5, 0), run_time=0.5)  # shape
        self.play(demo_gauss.animate.stretch(0.67, 0), run_time=0.5)
        self.play(demo_gauss.animate.set_fill(BLUE), run_time=0.4)  # color
        self.play(demo_gauss.animate.set_fill(RED), run_time=0.4)
        self.play(demo_gauss.animate.set_opacity(0.2), run_time=0.4)  # opacity
        self.play(demo_gauss.animate.set_opacity(0.7), run_time=0.4)

        self.wait(0.5)
        self.play(FadeOut(demo_gauss), FadeOut(props_title), FadeOut(props), FadeOut(step1))

        # ============ PART 2: Where do initial Gaussians come from? ============
        step2 = Text("Step 1: Get initial 3D points from your photos", font_size=26, color=WHITE)
        step2.to_edge(DOWN, buff=0.8)
        self.play(Write(step2))

        # Show photos
        photo1 = Rectangle(width=1.5, height=1.1, fill_color=GRAY_D, fill_opacity=0.8, stroke_color=WHITE)
        photo2 = photo1.copy()
        photo3 = photo1.copy()
        photo1.move_to(LEFT * 5 + UP * 1)
        photo2.move_to(LEFT * 5)
        photo3.move_to(LEFT * 5 + DOWN * 1)

        photo_label = Text("Your photos", font_size=16, color=GRAY_B)
        photo_label.next_to(photo2, LEFT, buff=0.3)

        # Simple object icon in each photo
        for p in [photo1, photo2, photo3]:
            icon = Circle(radius=0.2, fill_color=BLUE, fill_opacity=0.5, stroke_width=0)
            icon.move_to(p.get_center())
            p.add(icon)

        self.play(FadeIn(photo1), FadeIn(photo2), FadeIn(photo3), Write(photo_label))

        # Arrow to COLMAP
        arrow1 = Arrow(LEFT * 4, LEFT * 2.5, color=TURQUOISE, stroke_width=3)
        colmap_box = RoundedRectangle(width=2, height=1, corner_radius=0.1, fill_color="#1a1a2e", fill_opacity=0.9, stroke_color=TURQUOISE)
        colmap_box.move_to(LEFT * 1.5)
        colmap_text = Text("COLMAP", font_size=18, color=TURQUOISE)
        colmap_text.move_to(colmap_box)
        colmap_desc = Text("(finds matching\npoints in photos)", font_size=12, color=GRAY_B)
        colmap_desc.next_to(colmap_box, DOWN, buff=0.15)

        self.play(Create(arrow1), FadeIn(colmap_box), Write(colmap_text), Write(colmap_desc))

        # Arrow to sparse points
        arrow2 = Arrow(LEFT * 0.5, RIGHT * 1, color=TURQUOISE, stroke_width=3)
        self.play(Create(arrow2))

        # Show sparse point cloud
        sparse_points = VGroup()
        point_positions = [
            RIGHT * 2.5 + UP * 0.4,
            RIGHT * 3 + DOWN * 0.2,
            RIGHT * 2.8 + UP * 0.1,
            RIGHT * 3.3 + DOWN * 0.5,
            RIGHT * 2.3 + UP * 0.6,
            RIGHT * 3.5 + UP * 0.2,
        ]
        for pos in point_positions:
            dot = Dot(pos, radius=0.06, color=WHITE)
            sparse_points.add(dot)

        sparse_label = Text("Sparse 3D points", font_size=16, color=GRAY_B)
        sparse_label.next_to(sparse_points, DOWN, buff=0.4)

        self.play(LaggedStart(*[FadeIn(p, scale=3) for p in sparse_points], lag_ratio=0.1))
        self.play(Write(sparse_label))
        self.wait(0.5)

        # ============ PART 3: Initialize Gaussians at each point ============
        self.play(FadeOut(step2))
        step3 = Text("Step 2: Place a Gaussian at each point", font_size=26, color=WHITE)
        step3.to_edge(DOWN, buff=0.8)
        self.play(Write(step3))

        # Transform dots to Gaussians
        init_gaussians = VGroup()
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
        for i, pos in enumerate(point_positions):
            g = Ellipse(width=0.35, height=0.25, fill_color=colors[i], fill_opacity=0.6, stroke_width=0)
            g.move_to(pos)
            init_gaussians.add(g)

        self.play(
            *[ReplacementTransform(p, g) for p, g in zip(sparse_points, init_gaussians)],
            FadeOut(sparse_label),
            run_time=1
        )

        init_label = Text("Initial Gaussians\n(small, same size)", font_size=14, color=GRAY_B)
        init_label.next_to(init_gaussians, DOWN, buff=0.3)
        self.play(Write(init_label))
        self.wait(0.5)

        # Clear left side
        self.play(
            FadeOut(photo1), FadeOut(photo2), FadeOut(photo3), FadeOut(photo_label),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(colmap_box), FadeOut(colmap_text), FadeOut(colmap_desc),
            init_gaussians.animate.move_to(LEFT * 3),
            init_label.animate.move_to(LEFT * 3 + DOWN * 1.2),
        )

        # ============ PART 4: Training loop - COMPARE ============
        self.play(FadeOut(step3), FadeOut(init_label))
        step4 = Text("Step 3: Render image, compare to real photo", font_size=26, color=WHITE)
        step4.to_edge(DOWN, buff=0.8)
        self.play(Write(step4))

        # Render arrow
        render_arrow = Arrow(LEFT * 1.5, RIGHT * 0.5, color=BLUE, stroke_width=3)
        render_text = Text("Render", font_size=16, color=BLUE)
        render_text.next_to(render_arrow, UP, buff=0.1)
        self.play(Create(render_arrow), Write(render_text))

        # Rendered image (blurry/bad)
        rendered_frame = Rectangle(width=2, height=1.5, stroke_color=TURQUOISE, stroke_width=2, fill_color=GRAY_E, fill_opacity=0.3)
        rendered_frame.move_to(RIGHT * 2)
        rendered_label = Text("What Gaussians render", font_size=14, color=TURQUOISE)
        rendered_label.next_to(rendered_frame, UP, buff=0.15)

        # Add some blurry blobs inside to show it's rough
        rendered_blobs = VGroup()
        for i in range(4):
            b = Ellipse(width=0.4, height=0.3, fill_color=colors[i], fill_opacity=0.4, stroke_width=0)
            b.move_to(rendered_frame.get_center() + np.array([
                (np.random.rand() - 0.5) * 1.2,
                (np.random.rand() - 0.5) * 0.8,
                0
            ]))
            rendered_blobs.add(b)

        self.play(FadeIn(rendered_frame), Write(rendered_label), FadeIn(rendered_blobs))

        # Real photo (sharp)
        real_frame = Rectangle(width=2, height=1.5, stroke_color=GREEN, stroke_width=2, fill_color=GRAY_E, fill_opacity=0.3)
        real_frame.move_to(RIGHT * 5)
        real_label = Text("Actual photo", font_size=14, color=GREEN)
        real_label.next_to(real_frame, UP, buff=0.15)

        # Sharp object in real photo
        real_object = Circle(radius=0.4, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
        real_object.move_to(real_frame.get_center())

        self.play(FadeIn(real_frame), Write(real_label), FadeIn(real_object))

        # Compare arrow with LOSS
        vs_text = Text("vs", font_size=24, color=WHITE)
        vs_text.move_to(RIGHT * 3.5)
        self.play(Write(vs_text))

        loss_text = Text("LOSS = How different are they?", font_size=18, color=RED)
        loss_text.move_to(RIGHT * 3.5 + DOWN * 1.2)
        self.play(Write(loss_text))
        self.wait(0.5)

        # ============ PART 5: Optimization - adjust Gaussians ============
        self.play(FadeOut(step4))
        step5 = Text("Step 4: Adjust Gaussians to reduce the difference", font_size=26, color=WHITE)
        step5.to_edge(DOWN, buff=0.8)
        self.play(Write(step5))

        # Show adjustment arrows back to Gaussians
        adjust_arrow = CurvedArrow(
            loss_text.get_left() + LEFT * 0.2,
            init_gaussians.get_right() + RIGHT * 0.3,
            color=YELLOW, angle=PI/3
        )
        adjust_text = Text("Adjust position,\nsize, color, opacity", font_size=14, color=YELLOW)
        adjust_text.next_to(adjust_arrow, UP, buff=0.1)

        self.play(Create(adjust_arrow), Write(adjust_text))

        # Animate Gaussians adjusting
        for _ in range(2):
            self.play(
                *[g.animate.shift(np.array([np.random.rand()*0.1-0.05, np.random.rand()*0.1-0.05, 0]))
                  for g in init_gaussians],
                run_time=0.3
            )
        self.wait(0.3)

        # Clear for densification explanation
        self.play(
            FadeOut(rendered_frame), FadeOut(rendered_label), FadeOut(rendered_blobs),
            FadeOut(real_frame), FadeOut(real_label), FadeOut(real_object),
            FadeOut(render_arrow), FadeOut(render_text),
            FadeOut(vs_text), FadeOut(loss_text),
            FadeOut(adjust_arrow), FadeOut(adjust_text),
            FadeOut(step5),
            init_gaussians.animate.move_to(UP * 1.5),
        )

        # ============ PART 6: SPLIT, CLONE, PRUNE (one at a time) ============
        step6 = Text("Step 5: Add or remove Gaussians where needed", font_size=26, color=WHITE)
        step6.to_edge(DOWN, buff=0.8)
        self.play(Write(step6))

        # --- SPLIT ---
        split_title = Text("SPLIT", font_size=36, color=RED, weight=BOLD)
        split_title.move_to(UP * 1)
        split_desc = Text("Gaussian too big → divide into smaller ones", font_size=22, color=WHITE)
        split_desc.next_to(split_title, DOWN, buff=0.3)

        big_gauss = Ellipse(width=1.8, height=1.2, fill_color=RED, fill_opacity=0.6, stroke_width=0)
        big_gauss.move_to(DOWN * 1)

        self.play(Write(split_title), Write(split_desc), GrowFromCenter(big_gauss))
        self.wait(0.3)

        # Split animation
        small1 = Ellipse(width=0.9, height=0.6, fill_color=RED, fill_opacity=0.6, stroke_width=0)
        small2 = small1.copy()
        small1.move_to(LEFT * 1.2 + DOWN * 1)
        small2.move_to(RIGHT * 1.2 + DOWN * 1)

        self.play(
            ReplacementTransform(big_gauss, VGroup(small1, small2)),
            run_time=0.8
        )
        self.wait(0.5)

        # Clear SPLIT
        self.play(FadeOut(split_title), FadeOut(split_desc), FadeOut(small1), FadeOut(small2))

        # --- CLONE ---
        clone_title = Text("CLONE", font_size=36, color=BLUE, weight=BOLD)
        clone_title.move_to(UP * 1)
        clone_desc = Text("Area needs more detail → duplicate Gaussian", font_size=22, color=WHITE)
        clone_desc.next_to(clone_title, DOWN, buff=0.3)

        small_gauss = Ellipse(width=0.8, height=0.6, fill_color=BLUE, fill_opacity=0.6, stroke_width=0)
        small_gauss.move_to(LEFT * 0.8 + DOWN * 1)

        self.play(Write(clone_title), Write(clone_desc), GrowFromCenter(small_gauss))
        self.wait(0.3)

        # Clone animation
        clone_copy = small_gauss.copy()
        clone_copy.move_to(RIGHT * 0.8 + DOWN * 0.8)

        self.play(TransformFromCopy(small_gauss, clone_copy), run_time=0.8)
        self.wait(0.5)

        # Clear CLONE
        self.play(FadeOut(clone_title), FadeOut(clone_desc), FadeOut(small_gauss), FadeOut(clone_copy))

        # --- PRUNE ---
        prune_title = Text("PRUNE", font_size=36, color=GRAY_B, weight=BOLD)
        prune_title.move_to(UP * 1)
        prune_desc = Text("Gaussian nearly invisible → remove it", font_size=22, color=WHITE)
        prune_desc.next_to(prune_title, DOWN, buff=0.3)

        ghost_gauss = Ellipse(width=0.8, height=0.6, fill_color=GRAY, fill_opacity=0.15, stroke_width=2, stroke_color=GRAY)
        ghost_gauss.move_to(DOWN * 1)

        self.play(Write(prune_title), Write(prune_desc), FadeIn(ghost_gauss))
        self.wait(0.3)

        # Prune animation
        x_mark = Text("✗", font_size=48, color=RED)
        x_mark.move_to(ghost_gauss)
        self.play(Write(x_mark))
        self.play(FadeOut(ghost_gauss), FadeOut(x_mark), run_time=0.5)
        self.wait(0.3)

        # Clear PRUNE
        self.play(FadeOut(prune_title), FadeOut(prune_desc))

        # ============ PART 7: Final result ============
        self.play(FadeOut(step6))
        step7 = Text("After many iterations: Scene reconstructed!", font_size=26, color=WHITE)
        step7.to_edge(DOWN, buff=0.8)
        self.play(Write(step7))

        # Show dense final Gaussians
        self.play(
            FadeOut(init_gaussians),
        )

        final_gaussians = VGroup()
        for i in range(30):
            g = Ellipse(
                width=0.15 + np.random.rand() * 0.25,
                height=0.1 + np.random.rand() * 0.15,
                fill_color=colors[i % len(colors)],
                fill_opacity=0.4 + np.random.rand() * 0.4,
                stroke_width=0
            )
            g.move_to(np.array([
                (np.random.rand() - 0.5) * 4,
                (np.random.rand() - 0.5) * 2,
                0
            ]))
            g.rotate(np.random.rand() * PI / 2)
            final_gaussians.add(g)

        self.play(LaggedStart(*[GrowFromCenter(g) for g in final_gaussians], lag_ratio=0.03), run_time=1.5)

        # Final stats
        stats = VGroup(
            Text("Millions of Gaussians", font_size=20, color=WHITE),
            Text("Each with optimized: position, shape, color, opacity", font_size=16, color=GRAY_B),
            Text("→ Real-time rendering at 30+ FPS!", font_size=22, color=GREEN),
        )
        stats.arrange(DOWN, buff=0.2)
        stats.move_to(DOWN * 2)

        self.play(Write(stats[0]))
        self.play(Write(stats[1]))
        self.play(Write(stats[2]))

        self.wait(2)


# To render:
# manim -pql nerf_raymarching.py NeRFRayMarching
# manim -pqh nerf_raymarching.py NeRFRayMarching  (high quality)
# manim -pqh nerf_raymarching.py GaussianSplatting
# manim -pqh nerf_raymarching.py NeRFTraining
# manim -pqh nerf_raymarching.py GaussianSplattingTraining
