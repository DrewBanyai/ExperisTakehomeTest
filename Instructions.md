## SCORE A BOWLING GAME!
This coding challenge will task you to create a Python application that will score a bowling game. You can create this application with any Python Application framework you desire.


#### USER INTERFACE
There are 10 frames in bowling. The application should display all ten frames to the user. Each frame should be labeled with its frame number and contain two fields for the user to enter a score. 
Additionally, underneath the two fields for the user to enter their score, there should be a label that displays the user's score as of that frame.
All frames should be visible on screen. The example only shows the first couple for demonstration purposes.
A RESET button should exist at the bottom of the window. Pressing the RESET button should clear all scores and set the cursor to the very first input field in Frame 1.


#### VALID INPUT VALUES
* an "x" or an "X" for a value for a STRIKE
* an "/" for a spare
* the numbers 0-9 for each shot if it is not a strike or a spare
* the cursor should auto-advance to the next shot (or next frame in case of a strike)


#### LOGIC
* Every time the user keys in a value, the score should recalculate, and all of the scores UP TO the
currently played frame should display the score AS OF that frame (see example, Frame 1's score shows 8
because that was the score at the end of Frame 1, whereas Frame 2 shows 12 because at the point in
the game only one score was entered for Frame 2 and it made the total score a 12)
Frames 3-10 would be empty and not display any score using the above example because the game is in
the middle of Frame 2.
* Strike - if you knock down all 10 pins in the first shot of a frame, this is a strike. A strike is worth 10
points PLUS THE SUM OF YOUR NEXT TWO SHOTS.
* Spare - If you knock down all 10 pins using both shots of a frame, this is a spare. A spare is worth 10
points PLUS THE SUM OF YOUR NEXT ONE SHOT.
* Open frame - If you do not knock down all 10 pins using both shots of your frame (9 or fewer pins
knocked down), this is an open frame and is worth the number of pins knocked down.
* TENTH FRAME - The 10th frame is scored differently than the other 9. If you roll a strike in the first
shot of the 10th frame, you get 2 more shots. If you roll a spare in the first two shots of the 10th frame,
you get 1 more shot. If you leave the 10th frame open after two shots, the game is over and you do not
get an additional shot.
The score for the 10th frame is the total number of pins knocked down in the 10th frame.
This means that the 10th frame will require 3 input fields as opposed to only two like the other nine
frames.


#### EXAMPLE GAME
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8 / | 5 4 | 6 3 | X | X | 5 / | 5 3 | 7 2 | 3 / | 9 / X |
| 15 | 24 | 33 | 58 | 78 | 93 | 101 | 110 | 129 | 149 |

Frame 1 - a spare which is 10 plus the number of pins knocked over in the next shot which was 5, so 15 points.
Frame 2 - Open frame of 9 points, so add 9 to the previous score of 15 for 24.
Frame 3 - Open frame of 9 points, so add 9 to the previous score of 24 for 33.
Frame 4 - Strike - earn 10 points plus the sum of next two shots. In this case, the next two shots are a strike and a 5 which totals 15 pins, so 10 + 15 = 25 points earned for Frame 4 for a total of 58.
Frame 5 - Strike - earn 10 points plus the sum of next two shots. In this case, the next two shots are a 5 and a spare (a 5) which is a total of 10 pins so 10 + 10 = 20 and added to 58 gives a score of 78.
Frame 6 - a spare which is 10 plus the number of pins knocked over in the next shot which is 5 so 15 points added gives a score of 93.
Frame 7 - Open frame of 8 points, so add 8 to the previous score of 93 for 101.
Frame 8 - Open frame of 9 points, so add 9 to the previous score of 101 for 110.
Frame 9 - a spare which is 10 plus the number of pins knocked over in the next shot which is a 9, so 10+9 is 19 plus previous score of 110 gives the score 129.
Frame 10 - Last frame. A spare in the first two shots gives an extra roll, which is a strike. The score in the 10th frame is simply the number of pins knocked down total which is 20, giving a final score of 149.


#### CODING CONSIDERATIONS
You are free to program this application however you wish. Treat this code as if you were programming production code for a product.
The code should be tested and work as expected.
When completed, zip all of the source code (sln, csproj, cs, xaml etc... files) into a single file and submit.
It is also acceptable to upload to a repository (Github, etc.) and share the link to the project.