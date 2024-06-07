import manimhl as mhl
import manim as mn


class Example(mhl.SlideShow):
    def construct(self):
        self.init_canvas(show_slide_numbers=True)

        self.new_slide_title('ManimHL', author='César Godinho', date='03/06/2024')

        self.new_slide_subtitle('What is ManimHL?')

        self.begin_slide('Slide0')
        self.add_inline_text('ManimHL is just a simpler way to use manim to build pretty slideshows.')
        self.end_slide()

        self.new_slide_subtitle('Here are some examples of ManimHL...', 'But take them with a pinch of salt!')

        # Bullet list test
        self.begin_slide('Slide1')
        self.add_bullet('We can create bullets!')
        self.wait()
        self.add_bullet('We can also wait in between bullets!')
        self.wait()
        self.add_bullet('However they need to be single line to work properly =(')
        self.end_slide()

        # Inline text test
        self.begin_slide('Slide2')
        self.add_inline_text('This is inline text that the user can write at will. Linebreaks need to be manually specified.')
        self.add_inline_text('One can also add many instances of `add_inline_text`...')
        fig1 = self.add_inline_image('bimg.png', 'Some figure to test.')
        self.align_next_to(mn.RIGHT)
        self.add_inline_image('bimg.png', 'The same figure...')
        self.align_next_to(mn.RIGHT)
        self.add_inline_image('bimg.png', 'The same figure again...')
        self.align_retake_at(fig1)
        self.add_inline_text('This is some more text after the two figures:')
        self.begin_shift()
        self.add_bullet('Some')
        self.add_bullet('More')
        self.add_bullet('Topics')
        self.end_shift()
        self.add_inline_text('Finalizing with another sentence.')
        self.end_slide()

        self.new_slide_subtitle('The End', 'Or is it?', animateEnd=False)
