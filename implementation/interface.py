import tkinter as tk 
from tkinter import ttk
from playsound import playsound
import multiprocessing
from PIL import ImageTk, Image
import os
import shutil



# Colors of elements in the window 
bg_color = "#000000"
text_color = "white"

bg_b_color = "#ff1a75"
text_b_color ="black"
abg_b_color = "white"
atext_b_color = "#ff1a75"


# Melody parameters (GA parameters)
n_mel = 10              # Total number of melodies (pop_size)
n_eval = 10             # Range for fitness values: [1,...,n_eval]
n_rtm = 5            # Total number of rhythms
n_octaves = 1           # Number of octaves chosen by the user 

fitness = [0 for i in range(10)]
fitness_rhythm = [0 for i in range(5)]
final_melody = 1        # Index of the melody selected by the user, in [1,...,n_mel]
final_rhythm = 1        # Index of the rhythm selected by the user, in [1,..., n_rhythm]
rhythm_yn = False       # True if the user wants to try different rhythms
download_yn = False     # True if the user wants to download melody
download_yn_rtm = False # True if the user wants to download melody with modified rhythm
melody_selected = False # True when user selects the melody
rhythm_selected = False # True when user selects the rhythm
playing = False         # True when a melody is playing


# Main window creation
window = tk.Tk() 
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry("{}x{}".format(screen_width, screen_height))

window.title("Musical tracks evaluation")
window.resizable(False, False) # avoid window resize
window.configure(background=bg_color) 

# Font setup
my_font = "Arial"
size_1 = window.winfo_screenwidth()//96
size_2 = window.winfo_screenwidth()//109
size_3 = window.winfo_screenwidth()//128
size_4 = window.winfo_screenwidth()//153


"""             -------------  Initial frame   -------------            """

def window_initial():

    text0 = "Select options:"
    text0_output = tk.Label(window, text=text0, fg = text_color, bg= bg_color, font=(my_font, size_1))  
    text0_output.grid(row=0, column=0, sticky="W") 

    text1 = "Number of Octaves (default value = 1):"
    text1_output = tk.Label(window, text=text1, fg = text_color, bg= bg_color, font=(my_font, size_2))  
    text1_output.grid(row=1, column=0, sticky="W")

    text2 = "                                    "
    text2_output = tk.Label(window, text=text2, fg=text_color, bg=bg_color, font=(my_font, size_2)) 
    text2_output.grid(row=1, column=5, padx=20, sticky="W")

    # Buttons for the selection of the octaves 
    for i in range(3):
        button = tk.Button(text="             {}                 ".format(i+1), fg = text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground=abg_b_color, font=(my_font, size_3), command= lambda y=i: insert_octaves(y))
        button.grid(row=1, column=i+1, pady=10, sticky="W") 
    
    text3 = "Number of Melodies (default value = 10):"
    text3_output = tk.Label(window, text=text3, fg = text_color, bg= bg_color, font=(my_font, size_2))
    text3_output.grid(row=2, column=0, sticky="W")

    # Auxiliary function for the melodies combobox 
    def callfuncback(event):
        global n_mel
        text = "                               " # to ensure there are no artifacts
        text_output = tk.Label(window, text=text, fg = text_color, bg= bg_color, font=(my_font, size_2)) 
        text_output.grid(row=2, column=5)

        i = combo_mel.get()
        if (i == 0):
            text = "{}  melody".format(i)
        else: 
            text = "{}  melodies".format(i)

        text_output = tk.Label(window, text=text, fg = text_color, bg= bg_color, font=(my_font, size_2)) 
        text_output.grid(row=2, column=5)
        n_mel = int(i)

    # Combobox for the selection of the number of melodies
    combo_mel = ttk.Combobox(window, values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], width=10, font = (my_font, size_3))
    combo_mel.grid(row=2, column =1, sticky="W")
    combo_mel.current(9)
    combo_mel.bind("<<ComboboxSelected>>", callfuncback)

    # Button for the start of melodies generation
    botton_newgen = tk.Button(text="Start melody creation", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=quit_window)
    botton_newgen.grid(row=12, column=14, pady=10, padx=20, sticky="W") 


"""             -------------  Melody generation frame   -------------            """

def window_mel():
    global fitness
    fitness = [1 for i in range(n_mel)]

    text0 = "Track:"
    text0_output = tk.Label(window, text=text0, fg = text_color, bg= bg_color, font=(my_font, size_1))
    text0_output.grid(row=0, column=0, sticky="W") 

    text1 = "Evaluation:"
    text1_output = tk.Label(window, text=text1, fg = text_color, bg=bg_color,  font=(my_font, size_1)) 
    text1_output.grid(row=0, column=2, padx=20, sticky="W") 

    text2 = "Default score = 1        "
    text2_output = tk.Label(window, text=text2, fg = text_color, bg=bg_color,  font=(my_font, size_1)) 
    text2_output.grid(row=0, column=13, padx=20, sticky="W") 


    for i in range(n_mel):
        
        # Index of the generated melodies, starting from 1
        text3 = "{}".format(i+1)
        text3_output = tk.Label(window, text=text3, fg = text_color, bg=bg_color, font=(my_font, size_2)) 
        text3_output.grid(row=i+1, column=0, padx=30, sticky="W")

        # Buttons used to play the tracks 
        listen_button = tk.Button(text="Press to listen", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground=abg_b_color, font=(my_font, size_4), command= lambda y=i: play(y))
        listen_button.grid(row=i+1, column=1, pady=10, padx=20, sticky="W") 

        # Buttons for the evaluation of the tracks 
        for j in range(n_eval):
            button = tk.Button(text="{}".format(j+1), fg = text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground=abg_b_color, font=(my_font, size_4), command= lambda x=j+1, y=i: insert_score(x, y))
            button.grid(row=i+1, column=j+3, pady=10, sticky="W") 

    # Button for creating the new generation
    b_newgen = tk.Button(text="New generation", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=quit_window)
    b_newgen.grid(row=12, column=14, pady=10, padx=20, sticky="WENS")

    # Button for ending the melody generation phase 
    b_endgen = tk.Button(text="End melody generation", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=end_melody_sel)
    b_endgen.grid(row=12, column=15, pady=10, padx=20, sticky="WENS")


"""             -------------  Rhythm generation frame   -------------            """

def window_rhythm(): 
    global fitness_rhythm
    global n_rtm
    fitness_rhythm = [1 for i in range(n_rtm)]

    text0 = "Track:"
    text0_output = tk.Label(window, text=text0, fg = text_color, bg= bg_color, font=(my_font, size_1))
    text0_output.grid(row=0, column=0, sticky="W") 

    text1 = "Evaluation:"
    text1_output = tk.Label(window, text=text1, fg = text_color, bg=bg_color,  font=(my_font, size_1)) 
    text1_output.grid(row=0, column=2, padx=20, sticky="W") 

    text2 = "                                   "
    text2_output = tk.Label(window, text=text2, fg = text_color, bg=bg_color,  font=(my_font, size_2)) 
    text2_output.grid(row=0, column=13, padx=20, sticky="W") 


    for i in range(n_rtm):
        
        # Index of the generated rhythms, starting from 1
        text3 = "{}".format(i+1)
        text3_output = tk.Label(window, text=text3, fg = text_color, bg=bg_color, font=(my_font, size_2)) 
        text3_output.grid(row=i+1, column=0, padx=30, sticky="W")

        # Buttons used to play the tracks 
        listen_button = tk.Button(text="Press to listen", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground=abg_b_color, font=(my_font, size_4), command= lambda y=i: play(y))
        listen_button.grid(row=i+1, column=1, pady=10, padx=20, sticky="W") 

        # Buttons for the evaluation of the tracks 
        for j in range(n_eval):
            button = tk.Button(text="{}".format(j+1), fg = text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground=abg_b_color, font=(my_font, size_4), command= lambda x=j+1, y=i: insert_score_rtm(x, y))
            button.grid(row=i+1, column=j+3, pady=10, sticky="W") 

    # Button for creating the new generation
    b_newgen = tk.Button(text="New generation", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=quit_window)
    b_newgen.grid(row=12, column=14, pady=10, padx=20, sticky="WENS")

    # Button for ending the rhythm generation phase
    b_endgen = tk.Button(text="End rhythm generation", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=end_rhythm_sel)
    b_endgen.grid(row=12, column=15, pady=10, padx=20, sticky="WENS")


"""             -------------  Ending frame   -------------            """

def window_end():
    
    img = ImageTk.PhotoImage(Image.open("./images/MusicWallpaper.jpg"))
    img_panel = tk.Label(window, image = img, highlightthickness = 0, bd = 0)
    
    img_panel.photo = img
    img_panel.grid(row=2, column=1)

    text0 = "                                                       "
    text0_output = tk.Label(window, text=text0, fg = text_color, bg=bg_color, font=(my_font, size_2)) 
    text0_output.grid(row=0, column=0, padx=30, sticky="W")

    text1 = "                                  Your melody has been created, enjoy it!"
    text1_output = tk.Label(window, text=text1, fg = text_color, bg=bg_color, font=(my_font, size_2)) 
    text1_output.grid(row=1, column=1, padx=30, sticky="W")

    # End button
    b_end = tk.Button(text="    END     ", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=quit_window)
    b_end.grid(row=4, column=1, pady=10, padx=20, sticky="WENS")
    


"""             -------------  Functions recalled by buttons   -------------            """ 
         
# Show the currently selected number of octaves to the user
def insert_octaves(i):
    global n_octaves
    # To ensure there are no artifacts
    text = "                               "
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_2)) 
    text_output.grid(row=1, column=5, padx=20)

    if (i == 0):
        text = "{} octave".format(i + 1)
    else: 
        text = "{} octaves".format(i + 1)
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_2)) 
    text_output.grid(row=1, column=5, padx=20)
    n_octaves = i + 1


# Play the melody when the "Press to listen" button is clicked
def play(k):
    global playing
    global p
    if(playing == True):
        # Interrupt the currently playing melody if the user clicks a "Press to listen" button
        p.terminate()
        playing = False
    
    if(playing == False):
        p = multiprocessing.Process(target=playsound, args=("./audio/{}indiv.wav".format(k),))
        p.start()
        playing = True
    

# Show the currently selected scores for the melodies and rhythms 
def insert_score(n, i):
    global fitness
    fitness[i] = n
    text = "Current score: {}.   ".format(n)
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_2))
    text_output.grid(row=i+1, column=13, padx=20, sticky="W") 

# Show the currently selected scores for the melodies and rhythms 
def insert_score_rtm(n, i):
    global fitness_rhythm
    fitness_rhythm[i] = n
    text = "Current score: {}.   ".format(n)
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_2))
    text_output.grid(row=i+1, column=13, padx=20, sticky="W") 
    

# Close the window
def quit_window():

    global playing
    global p
    if(playing == True):
        # Interrupt the currently playing melody if the user clicks a button that changes window ("New gen" or "ok")
        p.terminate()
        playing = False
        
    for label in window.grid_slaves():
        label.grid_forget()
    window.quit()


# Allows to end the melody selection algorithm:
# - final melody selection 
# - ask the user if different rhythms should be generated
def end_melody_sel():
    global n_mel
    global final_melody
    global rhythm_yn

    text = "Select final melody"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=13, column=15, padx=20) 
    text = "Try different rhythm?"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=14, column=15, padx=20)
    text = "Select number of rhythms"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=15, column=15, padx=20)  
    text = "Download final melody?"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=16, column=15, padx=20) 

    # Auxiliary function for the final melody combobox
    def mel_index_sel(event):
        global final_melody
        f = combo_sel.get()
        final_melody = int(f)

    # Combobox for the selection of the final melody
    mel_index =['{}'.format(i + 1) for i in range(n_mel)]
    combo_sel = ttk.Combobox(window, values = mel_index, width=10, font = (my_font, size_3))
    combo_sel.grid(row=13, column =16, sticky="W")
    combo_sel.current(0)
    combo_sel.bind("<<ComboboxSelected>>", mel_index_sel)

    # Auxiliary function for the rhythm yes/no option combobox 
    def rhythm_decision(event):
        global rhythm_yn
        rhythm_yn_string = combo_rhythm.get()
        if (rhythm_yn_string == 'Yes'):
            rhythm_yn = True

    # Combobox for the rhythm yes/no option
    combo_rhythm = ttk.Combobox(window, values = ['Yes', 'No'], width=10, font = (my_font, size_3))
    combo_rhythm.grid(row=14, column =16, sticky="W")
    combo_rhythm.current(1)
    combo_rhythm.bind("<<ComboboxSelected>>", rhythm_decision)

    # Auxiliary function the number of rhythm combobox
    def n_rtm(event):
        global n_rtm
        n_rtm = int(combo_n_rtm.get())


    # Combobox for the number of rhythm to be evolved
    combo_n_rtm = ttk.Combobox(window, values = ['1', '2', '3', '4', '5'], width=10, font = (my_font, size_3))
    combo_n_rtm.grid(row=15, column =16, sticky="W")
    combo_n_rtm.current(4)
    combo_n_rtm.bind("<<ComboboxSelected>>", n_rtm)

    # Auxiliary function for the download yes/no option combobox 
    def download_decision(event):
        global download_yn
        download_yn_string = combo_download.get()
        if (download_yn_string == 'Yes'):
            download_yn = True

    # Combobox for the download yes/no option
    combo_download = ttk.Combobox(window, values = ['Yes', 'No'], width=10, font = (my_font, size_3))
    combo_download.grid(row=16, column =16, sticky="W")
    combo_download.current(1)
    combo_download.bind("<<ComboboxSelected>>", download_decision)

    b_ok = tk.Button(text="Ok!", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=ok_button_mel)
    b_ok.grid(row=17, column=16, pady=10, padx=20, sticky="WENS")


# Close the melody generation window, after the final melody selection
def ok_button_mel():
    global melody_selected
    melody_selected = True
    global final_melody
    
    global download_yn
    if download_yn:
        download_mel(final_melody - 1, False)
    
    quit_window()


# Allows to end the rhythm selection algorithm: final rhythm selection 
def end_rhythm_sel():
    global n_rtm
    global final_rhythm

    text = "Select final rhythm"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=13, column=15, padx=20) #mostriamo testo a fianco (colonna adiacente) a bottone

    text = "Download final rhythm?"
    text_output = tk.Label(window, text=text, fg=text_color, bg=bg_color, font=(my_font, size_3)) 
    text_output.grid(row=14, column=15, padx=20) 

    # Auxiliary function for the final rhythm combobox
    def rhythm_index_sel(event):
        global final_rhythm
        f = combo_sel.get()
        final_rhythm = int(f)

    # Combobox for the selection of the final rhythm
    rhythm_index =['{}'.format(i + 1) for i in range(n_rtm)]
    combo_sel = ttk.Combobox(window, values = rhythm_index, width=10, font = (my_font, size_3))
    combo_sel.grid(row=13, column =16, sticky="W")
    combo_sel.current(0)
    combo_sel.bind("<<ComboboxSelected>>", rhythm_index_sel)

    # Auxiliary function for the download yes/no option combobox 
    def download_decision(event):
        global download_yn_rtm
        download_yn_string = combo_download_rtm.get()
        if (download_yn_string == 'Yes'):
            download_yn_rtm = True

    # Combobox for the download yes/no option
    combo_download_rtm = ttk.Combobox(window, values = ['Yes', 'No'], width=10, font = (my_font, size_3))
    combo_download_rtm.grid(row=14, column =16, sticky="W")
    combo_download_rtm.current(1)
    combo_download_rtm.bind("<<ComboboxSelected>>", download_decision)

    b_ok = tk.Button(text="Ok!", fg=text_b_color, bg=bg_b_color, activeforeground=atext_b_color, activebackground= abg_b_color, font=(my_font, size_4), command=ok_button_rhythm)
    b_ok.grid(row=15, column=16, pady=10, padx=20, sticky="WENS")


# Close the rhythm generation window, after the final rhythm selection
def ok_button_rhythm():
    global rhythm_selected
    rhythm_selected = True
    global final_rhythm

    global download_yn_rtm
    if download_yn_rtm:
        download_mel(final_rhythm - 1, True)

    quit_window()


# Download the final melody, with and without rhythm selection
def download_mel(index, with_rtm):
    dirName = 'download'
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    source = "./audio/{}indiv.wav".format(index)
    if with_rtm:
        destination ="./download/my_melody_rtm.wav"
    else:
        destination ="./download/my_melody.wav"
    shutil.copy(source, destination)
    
"""
window_initial()

if __name__ == "__main__":
    window.mainloop() # Allows to start the script 

"""