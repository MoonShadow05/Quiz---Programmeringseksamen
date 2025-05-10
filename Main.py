import random
from Question import questions as ai_questions  # Import the list of questions from Question.py
from Question import Question  # Import the Question class
import wx  # Import wxPython for GUI

# Shuffle the questions to randomize their order
questions = [Question(q) for q in ai_questions]
random.shuffle(questions)

class MyFrame(wx.Frame):
    def __init__(self, questions):
        super().__init__(parent=None, title="Quiz with AI")  # Initialize the main frame
        self.questions = questions  # Store the list of questions
        self.current_question_index = 0  # Track the current question index

        # Get screen dimensions for setting the window size
        screen_width, screen_height = wx.GetDisplaySize()
        max_width = int(screen_width)
        max_height = int(screen_height)

        # Set the size and maximum size of the window
        self.SetSize((800, 600))
        self.SetMaxSize((max_width, max_height))

        # Create a panel to hold all GUI elements
        self.panel = wx.Panel(self)

        # Create buttons for the main menu
        self.start_button = wx.Button(self.panel, label="Start quizzen")
        self.exit_button = wx.Button(self.panel, label="Afslut")

        # Bind button events to their respective methods
        self.start_button.Bind(wx.EVT_BUTTON, self.BeginQuiz)
        self.exit_button.Bind(wx.EVT_BUTTON, self.Exit)

        # Display the main menu
        self.MainMenu()

    def MainMenu(self):

        # Create a welcome label
        label = wx.StaticText(self.panel, label="Velkommen til Quizzen!")
        label.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT,
                            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # Create a vertical sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, flag=wx.ALL, border=10, proportion=1)
        sizer.AddStretchSpacer(1)

        # Create buttons for starting the quiz and exiting
        start_button = self.start_button
        ExitButton = self.exit_button

        # Bind the buttons to their respective methods
        start_button.Bind(wx.EVT_BUTTON, self.BeginQuiz)
        ExitButton.Bind(wx.EVT_BUTTON, self.Exit)

        # Add buttons to a vertical sizer
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.Add(start_button, flag=wx.ALL, border=10)
        button_sizer.Add(ExitButton, flag=wx.ALL, border=10)

        # Add the button sizer to the main sizer
        sizer.Add(button_sizer, flag=wx.ALL | wx.EXPAND, proportion=1)

        # Set the sizer for the panel and fit it
        self.panel.SetSizerAndFit(sizer)
        self.Show()

    def BeginQuiz(self, event):
        # Reset the current question index to start the quiz
        self.current_question_index = 0
        self.panel.DestroyChildren()  # Clear the main menu
        self.DisplayQuestions()  # Display the first question

    def DisplayQuestions(self):
         # Clear the panel to display the new question
        self.panel.DestroyChildren()
        
        # Check if there are more questions
        if self.current_question_index >= len(self.questions):
            self.ShowResult()  # Show the results if all questions are answered
            return
        
        # Get the current question
        question = self.questions[self.current_question_index]
        options, self.correct_index = question.present_question()  # Get the options and correct answer index
        
        # Create a vertical sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Display the question text
        label = wx.StaticText(self.panel, label=question.question)
        label.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(label, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        
        # Create buttons for each answer option
        for i, option in enumerate(options):
            btn = wx.Button(self.panel, label=option)
            # Bind each button to the CheckAnswer method, passing the index of the selected option
            btn.Bind(wx.EVT_BUTTON, lambda event, idx=i: self.CheckAnswer(idx))
            sizer.Add(btn, flag=wx.ALL | wx.ALIGN_LEFT, border=5)  # Align buttons to the left
        
        # Optional: Add an "Exit Quiz" button
        exit_button = wx.Button(self.panel, label="Afslut quiz")
        exit_button.Bind(wx.EVT_BUTTON, self.Exit)
        sizer.Add(exit_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=10)  # Align the exit button to the right
        
        # Set the sizer for the panel and layout the elements
        self.panel.SetSizerAndFit(sizer)

    def CheckAnswer(self, user_index):
        # Check if the selected answer is correct
        correct = user_index == self.correct_index
        msg = "Korrekt!" if correct else f"Forkert! Det rigtige svar var: {self.questions[self.current_question_index].correct_answer}"
        wx.MessageBox(msg, "Resultat", wx.OK | wx.ICON_INFORMATION)
        # Move to the next question
        self.current_question_index += 1
        self.DisplayQuestions()  # Display the next question

    def ShowResult(self):
        # Clear the panel to display the results
        self.panel.DestroyChildren()

        # Display the final message
        label = wx.StaticText(self.panel, label="Quizzen er færdig – godt klaret!")
        label.SetFont(wx.Font(35, wx.FONTFAMILY_DEFAULT,
                              wx.FONTSTYLE.NORMAL, wx.FONTWEIGHT_BOLD))

        # Create a vertical sizer for layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, flag=wx.ALL, border=10)

        # Set the sizer for the panel and layout the elements
        self.panel.SetSizer(sizer)
        self.panel.Layout()

    def Exit(self, event):
        # Close the application
        self.Close()


# Main entry point for the application
if __name__ == "__main__":
    app = wx.App(False)  # Create the wxPython application
    frame = MyFrame(questions)  # Create the main frame with the list of questions
    app.MainLoop()  # Start the event loop