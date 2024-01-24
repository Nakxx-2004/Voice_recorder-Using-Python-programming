#This Program Is To Demonstrate Voice Recorder In Python Using Graphical User Interface
from tkinter import *
from tkinter import filedialog
import pygame
from mutagen.wave import WAVE
import tkinter.ttk as ttk
import glob
import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
from PIL import ImageTk,Image
from tkinter import simpledialog

splash_root = Tk()
# Adjust size
splash_root.geometry("1414x797")

#splash_root.geometry("200x200")
splash_root.overrideredirect(True)
cur_path = os.getcwd()

# Define image
bg = PhotoImage(file=cur_path+"C://Users//Admin//Desktop//Voice_Recorder//images//Voice_recorder.jpj")

# Create a canvas
my_canvas = Canvas(splash_root, width=1414, height=797, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)

# Set image in canvas
my_canvas.create_image(0,0, image=bg, anchor="nw")

def main():
    #destroy splash window
    splash_root.destroy()
    root =  Tk()
    root.title("Voice Recorder Using Python(Nakul Sharma)")
    root.image_0=Image.open("C://Users//Admin//Desktop//Voice_Recorder//images//Voice_recorder.jpj")
    root.geometry("880x680+375+45")
    root.iconbitmap()
    root.resizable(True,True)
    
    # Initialize Pygame
    pygame.mixer.init()
    cur_path = os.getcwd()
    
    # Create Function To Deal With Time
    def play_time():
            
            # Check to see if audios is stopped
            if stopped:
                    return
            
            # Grab Current audio's Time
            current_time = pygame.mixer.music.get_pos() / 1000

            # Convert audio's Time To Time Format
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            
            # Reconstruct audios with directory structure stuff
            audios = playlist_box.get(ACTIVE)
            val = None
            for evl in mylist:
                if audios+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    audios = val
                elif audios+'.wav' in evl:
                    val = evl
                    audios = val

            # Find Current Audio's Length
            song_mut = WAVE(audios)
            global song_length
            song_length = song_mut.info.length

            # Convert to time format
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
            
            # Check to see if audio is over
            if int(song_slider.get()) == int(song_length):
                    stop()

            elif paused:
                    # Check to see if paused, if so - pass
                    pass
            
            else: 
                    # Move slider along 1 second at a time
                    next_time = int(song_slider.get()) + 1

                    # Output new time value to slider, and to length of audios
                    song_slider.config(to=song_length, value=next_time)

                    # Convert Slider poition to time format
                    converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

                    # Output slider
                    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

            # Add Current Time To Status Bar
            if current_time > 0:
                    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
            
            # Create Loop To Check the time every second
            status_bar.after(1000, play_time)

    # Create Play Function
    def play():
            
            # Set Stopped to False since a audios is now playing
            global stopped
            stopped = False
            global mylist

            # Reconstruct audios with directory structure stuff
            audios = playlist_box.get(ACTIVE)            
            val = None
            for evl in mylist:
                if audios+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    audios = val
                elif audios+'.wav' in evl:
                    val = evl
                    audios = val
                    
            #Load audios with pygame mixer       
            pygame.mixer.music.load(audios)

            #Play audios with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Get audio's Time
            play_time()

    # Create Stopped Variable
    global stopped
    stopped = False 
    def stop():
            
            # Stop the audios
            pygame.mixer.music.stop()

            # Clear Playlist Bar
            playlist_box.selection_clear(ACTIVE)

            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')

            # Set our slider to zero
            song_slider.config(value=0)

            # Set Stop Variable To True
            global stopped
            stopped = True

    # Create Function To Play The Next audios
    def next_song():
            
            # Reset Slider position and status bar
            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')
            song_slider.config(value=0)

            #Get current audio's number
            next_one = playlist_box.curselection()

            # Add One To The Current audios Number Tuple/list
            next_one = next_one[0] + 1

            # Grab the audio's title from the playlist
            audios = playlist_box.get(next_one)

            # Add directory structure stuff to the audio's title
            audios = cur_path+'\{}'.format(audios)+'.wav'

            #Load audio's with pygame mixer
            pygame.mixer.music.load(audios)

            #Play audios with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Clear Active Bar in Playlist
            playlist_box.selection_clear(0, END)

            # Move active bar to next audios
            playlist_box.activate(next_one)

            # Set Active Bar To next audios
            playlist_box.selection_set(next_one, last=None)

    # Create function to play previous audios
    def previous_song():
            
            # Reset Slider position and status bar
            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')
            song_slider.config(value=0)

            #Get current audios number
            next_one = playlist_box.curselection()

            # Add One To The Current audios Number Tuple/list
            next_one = next_one[0] - 1

            # Grab the audios title from the playlist
            audios = playlist_box.get(next_one)

            # Add directory structure stuff to the audios title
            audios = cur_path+'\{}'.format(audios)+'.wav'

            #Load audios with pygame mixer
            pygame.mixer.music.load(audios)

            #Play audios with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Clear Active Bar in Playlist
            playlist_box.selection_clear(0, END)

            # Move active bar to next audios
            playlist_box.activate(next_one)

            # Set Active Bar To next audios
            playlist_box.selection_set(next_one, last=None)


    # Create Paused Variable
    global paused 
    paused = False

    # Create Pause Function
    def pause(is_paused):
            global paused
            paused = is_paused

            if paused:
                    #Unpause
                    pygame.mixer.music.unpause()
                    paused = False
            else:
                    #Pause
                    pygame.mixer.music.pause()
                    paused = True

    #Create Volume Function
    def volume(x):
            pygame.mixer.music.set_volume(volume_slider.get())

    # Create a Slide Function For audios Positioning
    def slide(x):
            
            # Reconstruct audios with directory structure stuff
            audios = playlist_box.get(ACTIVE)

            #audios = cur_path+'\{}'.format(audios)+'.wav'
            val = None
            for evl in mylist:
                if audios+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    audios = val
                elif audios+'.wav' in evl:
                    val = evl
                    audios = val
            
            #Load audios with pygame mixer
            pygame.mixer.music.load(audios)

            #Play audios with pygame mixer
            pygame.mixer.music.play(loops=0, start=song_slider.get())
    def Cloning(li1):
        li_copy = li1[:]
        return li_copy
    global out
    outname = []
    global fname
    fname = []
    def refresh():
            playlist_box.delete(0,END)
            mylist.append(retVal+"\\.wav")
            fname.append(retVal)
            out = os.path.basename(retVal)
            outname.append(out)
            mynewlist = Cloning(mylist)
            itlist = []
            num = 0
            n=int(len(fname))
            for y in mynewlist:
                for z in range(0,n):
                    if fname[z] in y:
                        y = y.replace(fname[z], outname[z])
                        itlist.append(y)
                        num += 1
            for h in range(num):
                mynewlist.pop()
            mynewlist.extend(itlist)
            for x in mynewlist:
                x = x.replace(cur_path+'\\',   "")
                x = x.replace("\\.wav", "")
                x = x.replace(".wav", "")
                
                playlist_box.insert(END,x)
            
    global recording
    recording = False
    def rec():
        global recording
        if recording:
            recording = False
            rec_button.config(image = rec_btn_img_on)       
            recstop_btn.config(image = recstop_btn_img_on)
            rec_button['command'] = rec
            recstop_btn['command'] = 0
            
        else:
            recording = True
            threading.Thread(target = record).start()
            rec_button.config(image = rec_btn_img_on)    
            recstop_btn.config(image = recstop_btn_img_on)
            rec_button['command'] = 0
            recstop_btn['command'] = rec
        
    def record():
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels =2,rate = 48000, input = True, frames_per_buffer=1024)
        frames = []
        start = time.time()
        while recording:
            data = stream.read(1024)
            frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed //60
            hours = mins // 60
            t_label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        t_label.config(text="00:00:00")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        #Create a new temporary "parent"
        newWin = Tk()

        #But make it invisible
        newWin.withdraw()

        #Now this works without throwing an exception:
        global retVal
        retVal=None
        retVal = filedialog.asksaveasfilename(initialdir=cur_path+'/',title="SAVE FILE AS",filetypes=(("WAV Files", "*.wav" ), ))

        #Destroy the temporary "parent"
        newWin.destroy()
        if retVal==None or retVal=='':
            return
        sound_file = wave.open(f""+retVal+".wav","wb")
        sound_file.setnchannels(2)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(48000)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()
        refresh()

        # Create Function To Add One audios To Playlist
    def delete_song():
            audios = filedialog.askopenfilename(initialdir=cur_path+'/', title="Choose A audios", filetypes=(("WAV Files", "*.wav" ), ))

            # Strip out directory structure and .wav from audios title
            #print(audios)
            mylist.append(audios)
            audios = os.path.basename(audios)

            #audios = audios.replace("C:/audio/", "")
            audios = audios.replace(".wav", "")

            # Add To End of Playlist
            playlist_box.insert(END, audios)

    # Create Function To Add Many Songs to Playlist
    def add_many_songs():
            songs = filedialog.askopenfilenames(initialdir=cur_path+'/', title="Choose A audios", filetypes=(("WAV Files", "*.wav" ), ))
            
            # Loop thru audios list and replace directory structure and WAV from audios name
            for audios in songs:
                    mylist.append(audios)
                    audios = os.path.basename(audios)
                    # Strip out directory structure and .wav from audios title
                    #audios = audios.replace("C:/audio/", "")
                    audios = audios.replace(".wav", "")
                    # Add To End of Playlist
                    playlist_box.insert(END, audios)

    # Create Function To Delete One audios From Playlist
    def delete_audio():
            
            # Delete Highlighted audios From Playlist
            remove = playlist_box.get(ANCHOR)
            for i in mylist:
                if remove in i:
                    mylist.remove(i)
            playlist_box.delete(ANCHOR)
            

    # Create Function To Delete All Songs From Playlist
    def delete_all_songs():
            # Delete ALL songs
            mylist.clear()
            playlist_box.delete(0, END)

            
    # Create main Frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill = BOTH, expand = True)

    # Create Playlist Box
    playlist_box = Listbox(main_frame, bg="black", fg="white", width=60, selectbackground="white", selectforeground="black",bd = 10,font=('arial',18))
    playlist_box.grid(row=0,column=0,columnspan=1,padx=25,pady=25)
    global mylist
    mylist = glob.glob(cur_path+"\*.wav")
    for x in mylist:
        x = x.replace(cur_path+'\\',   "")
        x = x.replace(".wav", "")      
        playlist_box.insert(END,x)

    # Style slider using ttk widget
    style = ttk.Style()
    style.configure("TScale", background="black")
    
    # Create volume slider frame
    volume_frame = LabelFrame(main_frame, text="VOLUME",font=('ds-digital',14),bg="black",fg="white")
    volume_frame.grid(row=1,column=0,sticky=E,padx=25)

    # Create Volume Slider
    toplabel=Label(volume_frame,text="+",bg="black",fg="white")
    toplabel.pack()
    volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=110, value=1, command=volume,style="TScale")
    volume_slider.pack()
    bottomlabel=Label(volume_frame,text="-",bg="black",fg="white")
    bottomlabel.pack()
    
    # Create audios Slider
    song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=455, value=0, command=slide,style="TScale")
    song_slider.grid(row=2, column=0, pady=10, padx=25, sticky=W)	

    # Define Button Images For Controls
    back_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//prev_img.png')
    forward_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//next_img.png')
    play_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//play_img.png')
    pause_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//pause_img.png')
    stop_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//stop_img.png')
    rec_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//speaking_off.png')         
    rec_btn_img_on = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//speaking_on.png')
    recstop_btn_img = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//rec_stop_off.png')    
    recstop_btn_img_on = PhotoImage(file=cur_path+'C://Users//Admin//Desktop//Voice_Recorder//images//rec_stop_on.png')
    
    # Create Button Frame
    control_frame = tk.Frame(main_frame,bg="black")
    control_frame.grid(row=1,column=0,sticky=W,padx=25)

    # Create Play/Stop etc Buttons
    back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song,bg="black")
    forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song,bg="black")
    play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play,bg="black")
    pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused),bg="black")
    stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop,bg="black")
    rec_button = Button(control_frame,image=rec_btn_img_on, borderwidth=0, command=rec,bg="black")       
    recstop_btn = Button(control_frame,image=recstop_btn_img_on, borderwidth=0, command=0,bg="black")
    
    back_button.grid(row=1, column=0, padx=30)
    forward_button.grid(row=1, column=1, padx=30)
    play_button.grid(row=1, column=2, padx=30)
    pause_button.grid(row=1, column=3, padx=30)
    stop_button.grid(row=1, column=4, padx=30)
    rec_button.grid(row=5, column=1, padx=30)       
    recstop_btn.grid(row = 5,column=3,padx =30)
    
    #timer
    t_label = Label(control_frame,text="00:00:00",font = ("ds-digital",20,"bold"),bg="black",fg="white")
    t_label.grid(row=2,column=0,rowspan=2,columnspan=6)

    # Create Status Bar
    status_bar = Label(main_frame,text='Time Elapsed: 00:00 of 00:00  ',font = ("ds-digital",22,"bold"), bd=1,bg="black",fg="white")
    status_bar.grid(row=4,column=0,sticky=SW,pady=30,padx=30)

    # Create Main Menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Create Add audios Menu Dropdows
    delete_song_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Add Audio", menu=delete_song_menu)

    # Add One audios To Playlist
    delete_song_menu.add_command(label="Add One Audio To Playlist", command=delete_song)
    
    # Add Many Songs to Playlist
    delete_song_menu.add_command(label="Add Many Audio To Playlist", command=add_many_songs)

    # Create Delete audios Menu Dropdowns
    remove_song_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Remove Audio", menu=remove_song_menu)
    remove_song_menu.add_command(label="Delete An Audio From Playlist", command=delete_audio)
    remove_song_menu.add_command(label="Delete All The Audio From Playlist", command=delete_all_songs)

    mainloop()
splash_root.after(5000,main)#1000 - 1SEC
# Execute tkinter
mainloop()