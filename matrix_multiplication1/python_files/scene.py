from types import BuiltinFunctionType
from manim import *

config.background_color = WHITE
Mobject.set_default(color = BLACK)
Text.set_default(font = "Ariel")
Matrix.set_default(left_bracket = "(", right_bracket = ")", h_buff = 0.8)
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

def writeEquation(listOfTerms):
    for i in range(len(listOfTerms)):
        if i != 0:
            listOfTerms[i].next_to(listOfTerms[i - 1])    
    return listOfTerms

# Initializing the three matrices in the equation we want to solve. Positioning the matrices. 
mL = IntegerMatrix([[2, 0], [1, 1]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
mR = IntegerMatrix([[2, 0, 0], [3, 4, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
mAnswer = Matrix([["4", "0", "0"], ["5", "4", "0"]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
tex = Tex("=")
mL.to_corner(UL)
for entry in mAnswer.get_entries():
    entry.set_opacity(0)
group = writeEquation(VGroup(mL, mR, tex, mAnswer))


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
        self.add_sound(r"C:\Users\siddh\Downloads\matrix_multiplication\2112.MatrixMultiplication.mp4")
        self.play(Write(group))
        self.wait(6)
        rekt = SurroundingRectangle(mAnswer.get_columns()[0])
        self.play(Write(rekt))
        self.wait(3.5)
        rekt1 = SurroundingRectangle(mR.get_columns()[0], color = GREEN)
        self.play(Write(rekt1))
        self.wait(1)
        self.play(moveMatrixRectangleColumn(mAnswer, rekt, 1))
        self.wait(2)
        self.play(moveMatrixRectangleColumn(mR, rekt1, 1))
        self.wait(2)
        self.play(moveMatrixRectangleColumn(mAnswer, rekt, 2))
        self.wait(2)
        self.play(moveMatrixRectangleColumn(mR, rekt1, 2))
        self.play(Unwrite(rekt), Unwrite(rekt1))

        self.wait(10)
        #Initializing the matrices/column-vectors used to carry out the computations: mL2 - another copy of the left-matrix used to show work,
        #c1, c2, c3 - the column vectors of mR
        #r1, r2, r3 - the column vectors of the answer to the problem, mAnswer
        mL2 = mL.copy()
        mL2.shift([4, -3, 0])
        c1 = IntegerMatrix([[2], [3]], left_bracket = "(", right_bracket = ")")
        c2 = IntegerMatrix([[0], [4]], left_bracket = "(", right_bracket = ")")
        c3 = IntegerMatrix([[0], [0]], left_bracket = "(", right_bracket = ")")
        tex2 = Tex("=")
        r1 = IntegerMatrix([[4], [5]], left_bracket = "(", right_bracket = ")")
        r2 = IntegerMatrix([[0], [4]], left_bracket = "(", right_bracket = ")")
        r3 = IntegerMatrix([[0], [0]], left_bracket = "(", right_bracket = ")")
        for entry in r1.get_entries():
            entry.set_opacity(0)

        #Highlighting the first column vector of mR, as we need to multiply this vector by mL 
        self.wait(8)
        rect = SurroundingRectangle(mR.get_columns()[0])
        self.play(Write(rect))


        #Computing the first column r1 of the result 
        step1 = writeEquation(VGroup(mL2.copy(), c1, tex2.copy(), r1.copy()))
        self.play(Write(step1))
        self.wait(3)
        self.play(step1[3].get_entries()[0].animate.set_opacity(1))
        self.wait(2.5)
        self.play(step1[3].get_entries()[1].animate.set_opacity(1))
        #Updating the first column of the matrix that is our answer, mAnswer
        self.play(updateMatrix(0, 0, "4", mAnswer), updateMatrix(1, 0, "5", mAnswer))

        #Doing the previous three steps for the second column
        self.play(Unwrite(step1))
        rect1 = SurroundingRectangle(mR.get_columns()[1])
        self.wait(1)
        self.play(rect.animate.move_to(rect1))
        self.wait(1)
        step2 = writeEquation(VGroup(mL2.copy(), c2, tex2.copy(), r2.copy()))
        self.play(Write(step2))
        self.wait(2)
        self.play(updateMatrix(0, 1, "0", mAnswer), updateMatrix(1, 1, "4", mAnswer))

        #Doing these steps for the third column
        self.wait(4)
        self.play(Unwrite(step2))
        rect2 = SurroundingRectangle(mR.get_columns()[2])
        self.play(rect.animate.move_to(rect2))
        self.wait(1)
        step3 = writeEquation(VGroup(mL2.copy(), c3, tex2.copy(), r3.copy()))
        self.play(Write(step3))
        self.wait(2)
        self.wait(6)
        self.play(updateMatrix(0, 2, "0", mAnswer), updateMatrix(1, 2, "0", mAnswer))
        self.wait(2)


class ThirdScene(Scene):
    def construct(self):
        group.center()
        self.play(Write(group))
        self.wait(2)
        matrixMultiplier(self, mL, mR, mAnswer, 2)


class FourthScene(Scene):
    def construct(self):
        mLF = Matrix([[1, 0], [0, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
        mLF.scale(0.6)
        mRF = Matrix([[1, 1], [0, 0]], left_bracket = "(", right_bracket = ")", h_buff = 0.8)
        mRF.scale(0.6)
        self.wait(1)
        tex1 = Tex(r"Suppose $A = $", font_size = 35)
        period = Tex(".")
        setup = writeEquation(VGroup(tex1, mLF, period))
        self.add(setup.to_corner(UL).to_edge(LEFT))
        self.wait(1)
        tex2 = Tex(r"""\begin{enumerate}
                   \item Give an example of a $2 \times 2$ matrix that does not commute with $A$. \\ 
                   \item Construct any non-zero matrices $B$ and $C$ so that $B \neq C$ but $AB = BC.$
                   \end{enumerate}
                   """, font_size = 35)
        tex2.move_to(tex1)
        tex2.shift([5, -1.2, 0])
        self.add(tex2)
        self.wait(1)
        tex3 = Tex(r"1) Take $B = $", font_size = 35)
        equals = MathTex("=", font_size = 35)
        firstSentencee = writeEquation(VGroup(tex3, mRF.copy(), period.copy())).to_edge(LEFT)
        self.play(Write(firstSentencee))
        

        mAnswerF = Matrix([["1", "1"], ["0", "0"]], left_bracket = '(', right_bracket = ')', h_buff = 0.8).scale(0.6)
        for entry in mAnswerF.get_entries():
            entry.set_opacity(0)
        tex4 = Tex("Then $AB = $", font_size = 35)
        counterexx1 = writeEquation(VGroup(tex4, mLF.copy(), mRF.copy(), equals.copy(), mAnswerF, period.copy()))
        self.play(Write(counterexx1.next_to(firstSentencee)))


        leftWork = counterexx1[1]
        rightWork = counterexx1[2]
        answer = counterexx1[4]
        matrixMultiplier(self, leftWork, rightWork, answer, 0.1)
        self.wait(2)
        tex5 = Tex("But $BA = $", font_size = 35)
        mAnswerG = Matrix([["1", "0"], ["0", "0"]]).scale(0.6)
        for entry in mAnswerG.get_entries():
            entry.set_opacity(0)
        counterexx2 = writeEquation(VGroup(tex5, mRF.copy(), mLF.copy(), equals.copy(), mAnswerG, period.copy()))
        self.play(Write(counterexx2.next_to(tex3, DOWN).shift([2.8, -0.3, 0])))
        self.wait(2)
        matrixMultiplier(self, counterexx2[1], counterexx2[2], counterexx2[4], 0.1)
        tex6 = Tex(r"$AB = B$ but $BA = A.$", font_size = 35).next_to(counterexx2)
        tex7 = Tex(r"Since $B \neq A$, $AB \neq BA$.", font_size = 35).next_to(tex3, DOWN).shift([1.5, -1.6, 0])
        self.play(Write(tex6))
        self.play(Write(tex7))

        self.play(Unwrite(tex7), Unwrite(tex6), Unwrite(counterexx2), Unwrite(counterexx1), Unwrite(firstSentencee))
        self.wait(2)




class FifthScene(Scene):
    def construct(self):
        
        period = Tex(".")
        tex1 = Tex(r"Suppose $A = $", font_size = 35)
        mLF = Matrix([[1, 0], [0, 0]]).scale(0.6)
        setup = writeEquation(VGroup(tex1, mLF, period))
        self.add(setup.to_corner(UL).to_edge(LEFT))
        tex2 = Tex(r"""\begin{enumerate}
                   \item Give an example of a $2 \times 2$ matrix that does not commute with $A$. \\ 
                   \item Construct any non-zero matrices $B$ and $C$ so that $B \neq C$ but $AB = BC.$
                   \end{enumerate}
                   """, font_size = 35)
        tex2.move_to(tex1)
        tex2.shift([5, -1.2, 0])
        self.add(tex2)
        
        equals = Tex("=")
        matrixB2 = Matrix([[0, 0], [0, 1]]).scale(0.6)
        matrixC2 = Matrix([[0, 0], [0, 2]]).scale(0.6)
        zeroMatrix = Matrix([[0, 0], [0, 0]]).scale(0.6)
        answerToTwo = writeEquation(VGroup(
            Tex("2) Take $B = $", font_size = 35), matrixB2, Tex(", $C = $", font_size = 35), 
            Matrix([[0, 0], [0, 2]]).scale(0.6), period.copy()
                                            ))
        answerToTwo.to_edge(LEFT)
        self.play(Write(answerToTwo))
        self.wait(2)
        mAnswerTwo = Matrix([[0, 0], [0, 0]]).scale(0.6)
        for entry in mAnswerTwo.get_entries():
            entry.set_opacity(0)
        writingoutAB2 = writeEquation(VGroup(
            Tex("$AB = $", font_size = 35), mLF.copy(), matrixB2.copy(), equals.copy(), mAnswerTwo.copy(), period.copy()
            ))
        writingoutAB2.next_to(answerToTwo, DOWN).shift([0.3, 0, 0])
        self.play(Write(writingoutAB2))
        matrixMultiplier(self, writingoutAB2[1], writingoutAB2[2], writingoutAB2[4], 0.1)
        writingoutAC2 = writeEquation(VGroup(
            Tex("$AC = $", font_size = 35), mLF.copy(), matrixC2.copy(), equals.copy(), mAnswerTwo.copy(), period.copy()
        ))
        writingoutAC2.next_to(answerToTwo, DOWN).shift([0.3, -1.3, 0])
        self.play(Write(writingoutAC2))
        matrixMultiplier(self, writingoutAC2[1], writingoutAC2[2], writingoutAC2[4], 0.1)
        self.wait(2)



            

        

def moveMatrixRectangleRow(matrix, rectangle, number):
    return rectangle.animate.move_to(SurroundingRectangle(matrix.get_rows()[number]))


def moveMatrixRectangleColumn(matrix, rectangle, number):
    return rectangle.animate.move_to(SurroundingRectangle(matrix.get_columns()[number]))


def matrixMultiplier(scene, matrixL, matrixR, answer, waitTime):
    rectL = SurroundingRectangle(matrixL.get_rows()[0])
    rectR = SurroundingRectangle(matrixR.get_columns()[0], color = GREEN)
    rowsL = len(matrixL.get_rows())
    colR = len(matrixR.get_columns())
    for i in range(rowsL):
        for j in range(colR):
            if (i == 0 and j == 0):
                scene.play(Write(rectL), Write(rectR))
                scene.wait(waitTime)
                scene.play(answer.get_rows()[i][j].animate.set_opacity(1))
                scene.wait(waitTime)
            else:
                scene.play(rectR.animate.move_to(SurroundingRectangle(matrixR.get_columns()[j])))
                scene.wait(waitTime)
                scene.play(answer.get_rows()[i][j].animate.set_opacity(1))
                scene.wait(waitTime)
        if (i != rowsL - 1):
            scene.play(moveMatrixRectangleRow(matrixL, rectL, i + 1),  rectR.animate.move_to(SurroundingRectangle(matrixR.get_columns()[0])))    
    
    scene.play(Unwrite(rectL), Unwrite(rectR))



    
    
