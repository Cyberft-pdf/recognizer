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
button_image_tr2 = pygame.transform.scale(backround_image, (1200, 800))
button_image_tr1 = pygame.transform.scale(start_img, (220, 145))
button_image_tr3 = pygame.transform.scale(button_img_net, (220, 145))
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

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_rect2 = pygame.Rect(button_x2, button_y2, button_width, button_height)


start_button_rect = button_img_net.get_rect()
start_button_rect2 = button_img_net.get_rect()
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
    command = "'color 2 & ipconfig /all" 
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

#NENÍ ZPOVOZNĚNO 
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
#NENÍ ZPOVOZNĚNO 


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
        WIN.blit(button_image_tr3, button_rect2,)                    
        WIN.blit(button_image_tr1, button_rect,)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            recognizer()

        elif button_rect2.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            my_network_information()

        elif button_rect2.collidepoint(mouse_pos) and mouse_pressed[0]:
            pygame.quit()  
            my_network_information()
    




    pygame.display.flip()

pygame.quit()