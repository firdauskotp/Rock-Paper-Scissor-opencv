import cv2 as cv
import cvzone
import cvzone as cvz
from cvzone.HandTrackingModule import HandDetector
import time, random

cap = cv.VideoCapture(0)

image_checker = 0
image_verify = 0

#pick background
background_choice = int(input("Which background would you like? \n 1. Normal \n 2. Nifl. \n Pick the number of the background you want \n"))

#setup camera size
cap.set(3, 640) #width
cap.set(4, 480) #height

#detector
detector = HandDetector(maxHands=1)

#timer
timer = 0
state_result = False
start_game = False

#score [AI, player]
score = [0, 0]

# if background_choice == 1:
#     image_checker = image_background
# else:
#     image_checker = image_background_nifl

# def game(background, start_game):
#     start_key = cv.waitKey(1)
#     if start_key == ord('s') or start_key == ord('S'):
#         start_game = True
#         initial_time = time.time()
#
#     success, img = cap.read()
#     img_scaled = cv.resize(img, (0, 0), None, 0.875, 0.875)
#     img_scaled = img_scaled[:, 80:480]
#
#     # find hands
#     hands, img = detector.findHands(img_scaled)
#
#     if start_game:
#
#         if state_result is False:
#             timer = time.time() - initial_time
#             cv.putText(background, str(int(timer)), (605, 435), cv.FONT_HERSHEY_PLAIN, 6, (255, 0, 0), 4)
#         if hands:
#             hand = hands[0]  # main hand
#             total_fingers = detector.fingersUp(hand)
#             print(total_fingers)
#
#     background[234:654, 795:1195] = img_scaled
#     cv.imshow("Background", background)



while True:
    image_background = cv.imread("./assets/BG.png")
    image_background_nifl = cv.imread("./assets/025_NiflPlain.png")
    success, img = cap.read()
    img_scaled = cv.resize(img,(0,0),None,0.875,0.875)
    img_scaled = img_scaled[:, 80:480]

    #find hands
    hands, img = detector.findHands(img_scaled)

    if start_game:

        if state_result is False:
            timer = time.time() - initial_time
            cv.putText(image_background, str(int(timer)),(605,435),cv.FONT_HERSHEY_PLAIN, 6, (255,0,0), 4)

            if timer > 3:
                state_result = True
                timer = 0
                if hands:
                    player_move = None
                    hand = hands[0] #main hand
                    total_fingers = detector.fingersUp(hand)
                    if total_fingers == [0,0,0,0,0]:
                        player_move = 1
                    if total_fingers == [1,1,1,1,1]:
                        player_move = 2
                    if total_fingers == [0,1,1,0,0]:
                        player_move = 3

                    random_number = random.randint(1,3)
                    opponent_image = cv.imread(f'assets/{random_number}.png', cv.IMREAD_UNCHANGED)
                    image_background = cvzone.overlayPNG(image_background, opponent_image, (149, 310))

                    #you win
                    if (player_move == 1 and random_number == 3) or (player_move == 2 and random_number == 1) or (player_move == 3 and random_number == 2):
                        score[1] += 1

                    # you lose
                    if (player_move == 3 and random_number == 1) or (player_move == 1 and random_number == 2) or (player_move == 2 and random_number == 3):
                        score[0] += 1


                    print("player move", player_move)
                    print("total fingers",total_fingers)

    if state_result:
        image_background = cvzone.overlayPNG(image_background, opponent_image, (149,310))

    cv.putText(image_background, str(score[0]), (410, 215), cv.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 5)
    cv.putText(image_background, str(score[1]), (1112, 215), cv.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 5)

    if background_choice == 1 or image_verify == 1:
        image_background[234:654, 795:1195] = img_scaled
        image_verify = 1
        image_checker = image_background
        cv.imshow("Background", image_background)
    elif background_choice == 2 or image_verify == 2:
        image_background_nifl[50:100, 50:100] = img_scaled
        image_verify = 2
        cv.imshow("Background", image_background_nifl)
        image_checker = image_background_nifl


    # image_background[234:654, 795:1195] = img_scaled
    # cv.imshow("Background", image_background)

    # cv.imshow("o hai you", img)
    # cv.imshow("Scaled Image", img_scaled)
    start_key = cv.waitKey(1)
    if start_key == ord('s') or start_key == ord('S'):
        start_game = True
        initial_time = time.time()
        state_result = False

    # game(image_checker, start_game)
