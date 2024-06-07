import manim as mn
from manim_slides import Slide


class SlideShow(Slide):
    def _update_canvas(self):
        self.slide_counter += 1
        if self.show_slide_numbers:
            slide_number_old = self.canvas['slide_number']
            slide_number_new = mn.Text(f'{self.slide_counter}').move_to(slide_number_old).scale(0.25)
            if self.slide_counter > 2:
                self.play(mn.Transform(slide_number_old, slide_number_new))
            else:
                self.canvas['slide_number'] = slide_number_new
                self.play(mn.FadeIn(slide_number_new))

    def _set_last_element(self, element):
        self.last_element = element

    def _align_element_to(self, element, to, align=mn.LEFT, buff=0.2):
        element = element.next_to(to, mn.DOWN, buff=buff)
        return element.align_to(to, align)

    def _align_element(self, element, align=mn.LEFT, buff=0.2):
        if self.last_element:
            if self.next_align is not None:
                element = element.next_to(self.last_element, self.next_align, buff=buff)
                self.next_align = None
            else:
                element = element.next_to(self.last_element, mn.DOWN, buff=buff)
                element = element.align_to(self.last_element, align).shift(mn.RIGHT * self.shift_env_val)
                if self.shift_env_val > 0.0:
                    self.shift_env_val = 0.0
        else:
            element = element.shift(mn.DOWN + (1.0 + self.shift_env_val) * mn.RIGHT)

        return element

    def _add_to_slide_stack(self, element):
        self.slide_stack.append(element)

    def init_canvas(self, show_slide_numbers=True, slide_text_scale=0.25):
        # Set slide counter
        self.slide_counter = 1

        # Set figure counter
        self.fig_count = 1

        # Next alignment overwrite
        self.next_align = None

        # Shift alignment env
        self.shift_env_val = 0.0
        self.last_shift_env_val = 0.0

        # Set the body slide text scale
        self.slide_text_scale = slide_text_scale

        # Set the last slide element
        # This is used on the add_* functions to know the last position
        self.last_element = None

        # Init the current subtitle to None
        self.curr_subtitle = None

        # Show slide numbers
        self.show_slide_numbers = show_slide_numbers
        if show_slide_numbers:
            slide_number = mn.Text('1').to_corner(mn.DR)
            self.add_to_canvas(slide_number=slide_number)

    # ------------------------------------
    # Slide creation functions
    # ------------------------------------

    def new_slide_title(self, title, author='', date='', Anim=mn.Write):
        mntitle = mn.Text(title).scale(2)
        self.add_to_canvas(title=mntitle)

        center = mntitle.get_center()
        line_start = center - [1.0, 0.0, 0.0]
        line_stop = center + [1.0, 0.0, 0.0]
        mnline = mn.Line(line_start, line_stop).next_to(mntitle, mn.DOWN)

        self.play(mn.Create(mnline), Anim(mntitle))

        if author != '':
            mnauthor = mn.Text(author).scale(0.5).next_to(mnline, mn.DOWN)
            self.play(Anim(mnauthor))

        if date != '':
            mndate = mn.Text(date).scale(0.5).next_to(mnauthor, mn.DOWN).shift(mn.DOWN)
            self.play(Anim(mndate))

        self.next_slide()
        self.play(mntitle.animate.scale(0.25).to_corner(mn.UL), mn.Unwrite(mnauthor), mn.Unwrite(mndate), mn.Unwrite(mnline))
        self._update_canvas()

    def new_slide_subtitle(self, subtitle, desc='', Anim=mn.Write, animateEnd=True):
        subtitle_new = mn.Text(subtitle).shift(mn.UP)
        if self.curr_subtitle:
            self.play(mn.Transform(self.curr_subtitle, subtitle_new))
        else:
            self.curr_subtitle = subtitle_new
            self.add_to_canvas(subtitle=self.curr_subtitle)
            self.play(Anim(self.curr_subtitle))

        if desc != '':
            mndesc = mn.Text(desc).scale(0.5).next_to(self.curr_subtitle, mn.DOWN)
            self.play(Anim(mndesc))

        self.next_slide()
        if animateEnd:
            if desc != '':
                self.play(self.curr_subtitle.animate.scale(0.5).to_corner(mn.UR), mn.Unwrite(mndesc))
            else:
                self.play(self.curr_subtitle.animate.scale(0.5).to_corner(mn.UR))
        self._update_canvas()

    def add_bullet(self, text):
        text = mn.Text(text).scale(self.slide_text_scale)
        bullet = mn.Circle(radius=0.025, color=mn.WHITE, fill_opacity=1).to_corner(mn.UL)

        bullet = self._align_element(bullet)
        text = text.next_to(bullet, mn.RIGHT, buff=0.1)

        self.play(mn.FadeIn(bullet), mn.Write(text))

        self._set_last_element(bullet)
        self._add_to_slide_stack(text)
        self._add_to_slide_stack(bullet)
        return bullet

    def add_inline_text(self, text):
        text = mn.Text(text).scale(self.slide_text_scale).to_corner(mn.UL)

        text = self._align_element(text)

        self.play(mn.Write(text))

        self._set_last_element(text)
        self._add_to_slide_stack(text)
        return text

    def add_inline_image(self, filename, caption='', scale=1.0):
        image = mn.ImageMobject(filename).scale(scale)
        self._add_to_slide_stack(image)

        if caption:
            text = mn.Text(f'Fig. {self.fig_count} - {caption}')
        else:
            text = mn.Text(f'Fig. {self.fig_count}')

        text = text.scale(self.slide_text_scale)
        text = self._align_element_to(text, image, align=[0, 0, 0], buff=0.05)

        border = mn.SurroundingRectangle(mn.Group(image, text), color=mn.WHITE, buff=0.05)

        self._align_element(mn.Group(image, text, border))

        self.play(mn.Write(text), mn.Create(border), mn.FadeIn(image))
        self.fig_count += 1

        self._add_to_slide_stack(text)

        self._set_last_element(border)
        self._add_to_slide_stack(border)
        return border

    # ------------------------------------
    # Object / Slideshow control functions
    # ------------------------------------

    def begin_slide(self, title=''):
        self.slide_stack = []

    def end_slide(self):
        self.next_slide()
        self.play((mn.FadeOut(e) for e in self.slide_stack))
        self.last_element = None
        self._update_canvas()

    def begin_shift(self, ammount=0.5):
        self.shift_env_val = ammount
        self.last_shift_env_val = ammount

    def end_shift(self):
        self.shift_env_val = -self.last_shift_env_val

    def wait(self):
        self.next_slide()

    def align_next_to(self, align):
        if sum(align - mn.DOWN) != 0:
            self.next_align = align

    def align_retake_at(self, obj):
        self._set_last_element(obj)
