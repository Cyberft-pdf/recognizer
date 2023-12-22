import tensorflow as tf
import cv2
import numpy as np
import json
from datetime import datetime
import pygame
import sys
import subprocess
import platform
import pywifi
from pywifi import const
import random 
import string 
import hashlib



pygame.init()
#Základní nastavení - začátek
WIDTH, HEIGHT = 1200,800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Recognizer")

#Základní nastavení- konec
pygame.init()
intro_image = pygame.image.load("pictures/intro_foto_rec.png")
intro_duration = 5000
intro_start_time = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()



#obrázky - začátek
backround_image = pygame.image.load("pictures/backround_image.png").convert_alpha()
start_img = pygame.image.load("pictures/start_button_face.png").convert_alpha()
button_img_net = pygame.image.load("pictures/button_net.png").convert_alpha()
button_img_pass = pygame.image.load("pictures/pixil-frame-0 (12).png").convert_alpha()
button_img_wifi = pygame.image.load("pictures/pixil-frame-0 (15).png").convert_alpha()
button_img_hash = pygame.image.load("pictures/pixil-frame-0 (17).png").convert_alpha()


button_image_tr2 = pygame.transform.scale(backround_image, (1200, 800))
button_image_tr1 = pygame.transform.scale(start_img, (220, 145))
button_image_tr3 = pygame.transform.scale(button_img_net, (220, 145))
button_image_tr4 = pygame.transform.scale(button_img_pass, (220, 145))
button_image_tr5 = pygame.transform.scale(button_img_wifi, (220, 145))
button_image_tr6 = pygame.transform.scale(button_img_hash, (220, 145))


#obrázky - konec

#velikost tlačítka - začátek
button_width = 190
button_widt2 = 400
button_height = 115
button_height2 = 600

button_x = (button_height) // 1
button_y = (button_height2) // 1

button_x2 =  400
button_y2 =  590

button_x3 =  658
button_y3 =  590

button_x4 =  900
button_y4 =  590

button_x5 =  950
button_y5 =  590

button_x6 =  930
button_y6 =  420

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_rect2 = pygame.Rect(button_x2, button_y2, button_width, button_height)
button_rect3 = pygame.Rect(button_x3, button_y3, button_width, button_height)
button_rect4 = pygame.Rect(button_x4, button_y4, button_width, button_height)
button_rect5 = pygame.Rect(button_x5, button_y5, button_width, button_height)
button_rect6 = pygame.Rect(button_x6, button_y6, button_width, button_height)


start_button_rect = button_img_net.get_rect()
start_button_rect2 = button_img_net.get_rect()
start_button_rect3 = button_img_net.get_rect()

#velikost tlačítka - konec


#když tak pro napsání textu / nevyužito
def draw_text(text, font, text_col, x, y,):
  img = font.render(text, True, text_col)
  WIN.blit(img, (x, y))

#Rozpoznávání
def recognizer():
    data_list = []
    model_gender = tf.keras.models.load_model("model2.h5")  
    model_age =tf.keras.models.load_model("model3.h5")


    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()  

        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = frame[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            face = face / 255.0
            face = np.expand_dims(face, axis=0)

            predictions_gender = model_gender.predict(face)
            predictions_age = model_age.predict(face)

            gender_label = np.argmax(predictions_gender, axis=0 )[0]

            #díky tomuto to funguje 
            female_probability = predictions_gender[0][0]
            old_probability = predictions_age[0][0]

            if female_probability > 0.5:
                gender = "Female"

            else:
                gender = "Male"

            if old_probability > 0.5:
                age = "Young"                 
            
            else:
                age = "Old"

            data_list.append({
                            "gender": gender, 
                            "age": age,
                            "date/time": datetime.now().isoformat(),                          
                            })



            cv2.putText(frame, f'Gender: {gender}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"Age: {age}", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)


        cv2.imshow("Live Detekce a Rozpoznávání Pohlaví", frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            with open("data.json", "a") as json_file:
                json.dump(data_list, json_file, indent=4)
                json_file.write("\n")
            break


    cap.release()
    cv2.destroyAllWindows()

def my_network_information():
    command = "color 2 & ipconfig /all" 
    command = f"color 2 & {command}"

    subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        output = result.stdout
        error = result.stderr
        
        print("Výstup z příkazu:")
        print(output)
        
        if error:
            print("Chyba:")
            print(error)
    except subprocess.CalledProcessError as e:
        print(f"Chyba při spuštění příkazu: {e}")


def wifi_okoli():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  

    iface.scan() 
    iface.scan_results()

    scan_results = iface.scan_results()
    print("-------------------------------------")
    print(" ")
    for result in scan_results:
        ssid = result.ssid
        signal_strength = result.signal
        print(f"SSID: {ssid}, Signál: {signal_strength} dBm")
        print(" ") 
        print("-------------------------------------")   

def gen_pasword():
    site = input("What website or app:")
    email = input("What is the email/username:")

    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choice(characters) for i in range(length))
        return password

    generate_password = generate_password()

    with open("password_manager.txt", "a") as f:
        data = site, email, generate_password
        f.write( "\n")
        f.write(str(data))
        f.write("\n")


    print(f"New password is: {generate_password}")
    
def hash():
    # A string that has been stored as a byte stream
    # (due to the prefix b)
    string = input("Enter string you want to hash: ")
    binary_string = string.encode('utf-8')

    # Initializing the sha256() method
    sha256 = hashlib.sha256()

    # Passing the byte stream as an argument
    sha256.update(binary_string)

    # sha256.hexdigest() hashes all the input data
    # passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which all
    # the input data gets hashed
    # hexdigest() hashes the data, and returns
    # the output in hexadecimal format
    string_hash = sha256.hexdigest()


    print(f"Hash:{string_hash}")

    otazka = input("Do you want to store the hash? y/n")

    if otazka == "y":
        print("done")
        with open("hash.txt", "a") as f:
            data = string, string_hash
            f.write( "\n")
            f.write(str(data))
            f.write("\n")
    elif otazka == "n":
        print("then remeber it!")

    else:
        print("Bad choice :( ")


#hlavní while loop
show_intro = True
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    current_time = pygame.time.get_ticks()
    #začatek PL_foto
    if show_intro:
            WIN.blit(intro_image, (0, 0))
            pygame.display.flip()

            if current_time - intro_start_time >= intro_duration:
                show_intro = False

    else:
        WIN.blit(button_image_tr2, (0, 0))   
        WIN.blit(button_image_tr1, button_rect,)
        WIN.blit(button_image_tr3, button_rect2,)                    
        WIN.blit(button_image_tr1, button_rect,)
        WIN.blit(button_image_tr5, button_rect3,)
        WIN.blit(button_image_tr4, button_rect5,)
        WIN.blit(button_image_tr6, button_rect6,)
        

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            recognizer()

        elif button_rect2.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            my_network_information()

        elif button_rect3.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            wifi_okoli()            

        elif button_rect5.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            gen_pasword()

        elif button_rect6.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            hash()

    pygame.display.flip()

pygame.quit()
