from types import BuiltinFunctionType
from manim import *

config.background_color = WHITE
Mobject.set_default(color = BLACK)
Text.set_default(font = "Ariel")
template1 = TexTemplate()
template1.preamble = r"""
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
"""
Tex.set_default(tex_template = template1)


#Method to update a particular entry in a matrix 
def updateMatrix(i, j, newVal, matrix):
    return ReplacementTransform(matrix.get_rows()[i][j], MathTex(newVal).move_to(matrix.get_rows()[i][j]))

# Initializing the three matrices in the equation we want to solve. Positioning the matrices. 
mL = IntegerMatrix([[2, 0], [1, 1]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
mR = IntegerMatrix([[2, 0, 0], [3, 4, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
mAnswer = Matrix([["?", "?", "?"], ["?", "?", "?"]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
tex = Tex("=")
mL.to_corner(UL)
mR.next_to(mL, RIGHT)
tex.next_to(mR, RIGHT)
mAnswer.next_to(tex, RIGHT)
group = VGroup(mL, tex, mR, mAnswer)


class FirstScene(Scene):
    def construct(self):
        tex = Tex(
            r"\raggedright{Definition:}",
            r"""
            \raggedright{Let $A$ be an $m\times{n}$ matrix, and $B$ be a $n\times{p}$ matrix. 
            The product is $AB$, an $m\times{p}$ matrix equal to}
            """,
            r"""
            $${AB = A\biggl(\vec{b_1}\,\,\,.\,.\,.\,\,\,\vec{b_p}\biggr) = \biggl(A\vec{b_1}\,\,\,.\,.\,.\,\,\,A\vec{b_p}\biggr)}$$
            """,
            font_size = 36)
        tex[0].set_color(RED)
        tex.to_corner(UL)
        rectangle = SurroundingRectangle(tex, color=BLACK)
        self.add(rectangle)
        self.play(Write(tex))  
        tex2 = Tex(r"\raggedright{Example:}",
            r"""
            \raggedright{Compute the following product.}

            """,
            r"""
            $$C = AB = \begin{pmatrix} 2 & 0 \\ 1 & 1 \\ \end{pmatrix} \begin{pmatrix} 2 & 0 & 0 \\ 3 & 4 & 0 \end{pmatrix}$$
            """, font_size = 36)
        tex2[0].set_color(YELLOW)
        tex2.to_corner(UL).shift([0, -4.2, 0])
        self.play(Write(tex2))
        self.wait(5)


class SecondScene(Scene):
    def construct(self):
        #Displaying this equation on the canvas
        self.play(Write(group))
        self.wait(2)

        #Initializing the matrices/column-vectors used to carry out the computations: mL2 - another copy of the left-matrix used to show work,
        #c1, c2, c3 - the column vectors of mR
        #r1, r2, r3 - the column vectors of the answer to the problem, mAnswer
        mL2 = mL.copy()
        mL2.shift([4, -3, 0])
        c1 = IntegerMatrix([[2], [3]], left_bracket = "(", right_bracket = ")")
        c2 = IntegerMatrix([[0], [4]], left_bracket = "(", right_bracket = ")")
        c3 = IntegerMatrix([[0], [0]], left_bracket = "(", right_bracket = ")")
        c1.next_to(mL2, RIGHT)
        c2.next_to(mL2, RIGHT)
        c3.next_to(mL2, RIGHT)
        tex2 = Tex("=")
        tex2.next_to(c1, RIGHT)
        r1 = IntegerMatrix([[4], [5]], left_bracket = "(", right_bracket = ")")
        r1.next_to(tex2, RIGHT)
        r2 = IntegerMatrix([[0], [4]], left_bracket = "(", right_bracket = ")")
        r2.next_to(tex2, RIGHT)
        r3 = IntegerMatrix([[0], [0]], left_bracket = "(", right_bracket = ")")
        r3.next_to(tex2, RIGHT)

        #Highlighting the first column vector of mR, as we need to multiply this vector by mL 
        rect = SurroundingRectangle(mR.get_columns()[0])
        self.play(Write(rect))
        self.wait(2)


        #Computing the first column r1 of the result 
        step1 = VGroup(mL2.copy(), c1, tex2.copy(), r1.copy())
        self.play(Write(step1))
        self.wait(2)

        #Updating the first column of the matrix that is our answer, mAnswer
        self.play(updateMatrix(0, 0, "4", mAnswer), updateMatrix(1, 0, "5", mAnswer))

        #Doing the previous three steps for the second column
        self.play(Unwrite(step1))
        rect1 = SurroundingRectangle(mR.get_columns()[1])
        self.play(rect.animate.move_to(rect1))
        self.wait(1)
        step2 = VGroup(mL2.copy(), c2, tex2.copy(), r2.copy())
        self.play(Write(step2))
        self.wait(2)
        self.play(updateMatrix(0, 1, "0", mAnswer), updateMatrix(1, 1, "4", mAnswer))

        #Doing these steps for the third column
        self.play(Unwrite(step2))
        rect2 = SurroundingRectangle(mR.get_columns()[2])
        self.play(rect.animate.move_to(rect2))
        self.wait(1)
        step3 = VGroup(mL2.copy(), c3, tex2.copy(), r3.copy())
        self.play(Write(step3))
        self.wait(2)
        self.play(updateMatrix(0, 2, "0", mAnswer), updateMatrix(1, 2, "0", mAnswer))
        self.wait(2)


class ThirdScene(Scene):
    def construct(self):
        group.center()
        self.play(Write(group))
        self.wait(2)
        rect = SurroundingRectangle(mR.get_columns()[0])
        rect1 = SurroundingRectangle(mL.get_rows()[0], color = GREEN)
        answerArray = [["4", "0", "0"], ["5", "4", "0"]]
        for i in range(2):
            for j in range(3):
                if (i == 0 and j == 0):
                    self.play(Write(rect), Write(rect1))
                    self.wait(2)
                    self.play(updateMatrix(0, 0, "4", mAnswer))
                    self.wait(2)
                else:
                    self.play(moveMatrixRectangleColumn(mR, rect, j))
                    self.wait(2)
                    self.play(updateMatrix(i, j, answerArray[i][j], mAnswer))
                    self.wait(2)
            if (i == 0):
                self.play(moveMatrixRectangleRow(mL, rect1, 1), moveMatrixRectangleColumn(mR, rect, 0))


class FourthScene(Scene):
    def construct(self):
        self.wait(1)
        tex1 = Tex(r"Suppose $A = \begin{pmatrix}1 & 0 \\ 0 & 0 \end{pmatrix}.$", font_size = 35)
        tex1.to_corner(UL)
        self.add(tex1)
        self.wait(1)
        tex2 = Tex(r"""\begin{enumerate}
                   \item Give an example of a $2 \times 2$ matrix that does not commute with $A$. \\ 
                   \item Construct any non-zero matrices $B$ and $C$ so that $B \neq C$ but $AB = BC.$
                   \end{enumerate}
                   """, font_size = 35)
        tex2.move_to(tex1)
        tex2.shift([4.5, -1.2, 0])
        self.add(tex2)
        self.wait(1)
        tex3 = Tex(r"1) Take $B = \begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}$. Then $AB = $", font_size = 35)
        mLF = Matrix([[1, 0], [0, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
        mLF.scale(0.6)
        mLF.next_to(tex3, RIGHT)
        mRF = Matrix([[1, 1], [0, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
        mRF.scale(0.6)
        
        mRF.next_to(mLF, RIGHT)
        equals = MathTex("=").next_to(mRF)
        mAnswerF = MathTex(r"\begin{pmatrix} & \\ & \end{pmatrix}")
        mAnswerF.next_to(equals, RIGHT)
        counterex1 = VGroup(tex3, mLF, mRF, equals, mAnswerF)
        counterex1.to_edge(LEFT)
        self.play(Write(counterex1))
        self.wait(2)
        

def moveMatrixRectangleRow(matrix, rectangle, number):
    return rectangle.animate.move_to(SurroundingRectangle(matrix.get_rows()[number]))


def moveMatrixRectangleColumn(matrix, rectangle, number):
    return rectangle.animate.move_to(SurroundingRectangle(matrix.get_columns()[number]))






    
    
