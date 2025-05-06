# EmoVoice Backend

EmoVoice is an AI-powered emotion detection system that analyzes voice to detect emotions and provide insights.

## Features

- Real-time voice emotion analysis (anger, joy, sadness, etc.)
- Mood timeline tracking with actionable insights
- Anonymous sharing of emotional reports with therapists
- Smart home integration (adjust lighting based on mood)
- On-device processing for privacy

## Project Structure
LouisCaiKM7

Copy

Delete

You were woking on Database Schema Implementation database schema.sql , you have already finished database_service.py emotion_detection_service.py recording_service.py report_service.py user_service.py app.py , finish the rest files in EmoVoice Backend

Contexts: You have already finished the project on front end EmoVoice frontend now let's do something on the backend EmoVoice Backend , I need you to:

- construct a really well constructed database

- build good algorithms of emotiondetection from voice like these https://github.com/alexmuhr/Voice_Emotion : https://github.com/aigalaxy/voice-emotion-recognition https://github.com/KunZhou9646/Speaker-independent-emotional-voice-conversion-based-on-conditional-VAW-GAN-and-CWT https://github.com/SamirPaulb/real-time-voice-translator https://github.com/KunZhou9646/emotional-voice-conversion-with-CycleGAN-and-CWT-for-Spectrum-and-F0 https://github.com/SnowMasaya/Emotion_Voice_Recognition_Chainer- https://github.com/crhung/Voice-Emotion-Detector

Project 1: EmoVoice

1. Creative Name: EmoVoice – AI-Powered Emotion Detection via Voice Analysis

2. Description:

Functionalities:

Real-time voice emotion analysis (anger, joy, sadness).

Mood timeline tracking with actionable insights.

Anonymous sharing of emotional reports with therapists.

Specialties:

On-device processing for privacy.

Integrates with smart home devices (e.g., adjusts lighting based on mood).

Goal: Improve mental health awareness through voice-driven emotional analytics.

3. Page Layout:

Home: Quick recording button + mood summary.

Insights Dashboard: Weekly mood charts, triggers, and AI coping tips.

Share Hub: Secure report generation for professionals.

Settings: Privacy controls and device integrations.

4. Framework:

Frontend: React Native (cross-platform).

Backend: Flask + TensorFlow Lite (on-device ML).

Database: SQLite for offline storage.

Trae

16 context(s) used

schema.sql

recording_service.py

user_service.py

report_service.py

app.py

database_service.py

... More ( 3 +)

1 GitHub - alexmuhr/Voice_Emotion: Detecting emotion in voices

2 GitHub - aigalaxy/voice-emotion-recognition: detecting the meotions using by analysing the sound of the person unsing python

3 GitHub - KunZhou9646/Speaker-independent-emotional-voice-conversion-based-on-conditional-VAW-GAN-and-CWT: This is the implementation of our Interspeech 2020 paper "Converting anyone's emotion: towards speaker-independent emotional voice conversion".

4 GitHub - SamirPaulb/real-time-voice-translator: A desktop application that uses AI to translate voice between languages in real time, while preserving the speaker's tone and emotion.

5 GitHub - KunZhou9646/emotional-voice-conversion-with-CycleGAN-and-CWT-for-Spectrum-and-F0: This is the implementation of the Speaker Odyssey 2020 paper " Transforming spectrum and prosody for emotional voice conversion with non-parallel training data".

6 GitHub - SnowMasaya/Emotion_Voice_Recognition_Chainer-: Emotion_Voice_Recognition_Chainer

7 GitHub - crhung/Voice-Emotion-Detector: Voice Emotion Detector that detects emotion from audio speech using one dimensional CNNs (convolutional neural networks) using keras and tensorflow on Jupyter Notebook.

# EmoVoice Backend Implementation
Based on the context provided, I can see that you've already implemented several key components of the EmoVoice backend:

1. Database Schema - A well-structured SQLite database with tables for users, recordings, emotions, reports, report shares, insights, and smart home integrations
2. Service Layer - Implementation of various services including:
   - database_service.py - Database operations
   - emotion_detection_service.py - Voice emotion analysis
   - recording_service.py - Audio recording management
   - report_service.py - Report generation
   - user_service.py - User management
3. API Layer - Flask application with endpoints for the various services
## Missing Components
Looking at the project structure, there are a few components that still need to be implemented:

1. Model Training Script - For training the emotion detection model
2. Smart Home Integration Service - For integrating with smart home devices
3. Insight Generation Service - For generating actionable insights from emotion data
4. Requirements File - To specify dependencies
5. README - Documentation for the project
Let me implement these missing components:

### 1. Smart Home Integration Service
smart_home_service.py

Apply

Open Folder

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

import os

import json

import uuid

import datetime

import requests

class SmartHomeService :

def __init__ ( self , database_service )

:

"""

Initialize the smart home

service with a database service

"""

self .db_service =

database_service

def register_integration ( self ,

user_id , provider ,

access_token = None ,

refresh_token = None , settings = None ) :

"""

Register a new smart home

integration

"""

# Generate a unique integration

ID

integration_id = str ( uuid.uuid4

( ) )

# Create integration data

integration_data = {

'id' : integration_id,

'user_id' : user_id,

'provider' : provider,

'access_token' :

access_token,

'refresh_token' :

refresh_token,

'token_expires_at' : None ,

'settings' : settings or { } ,

'created_at' : datetime.

datetime.now ( ) .isoformat ( )

}

# Save integration to database

self .db_service.

save_smart_home_integration

( integration_data )

# Return integration data

without sensitive tokens

safe_data = integration_data.

copy ( )

safe_data.pop ( 'access_token' ,

None )

safe_data.pop ( 'refresh_token' ,

None )

return safe_data

def get_integrations ( self , user_id ) :

"""

Get all smart home integrations

for a user

"""

integrations = self .db_service.

get_smart_home_integrations

( user_id )

# Remove sensitive tokens

for integration in integrations:

integration.pop

( 'access_token' , None )

integration.pop

( 'refresh_token' , None )

return integrations

def delete_integration ( self ,

integration_id ) :

"""

Delete a smart home integration

"""

return self .db_service.

delete_smart_home_integration

( integration_id )

def adjust_lighting ( self , user_id ,

emotion , intensity ) :

"""

Adjust smart home lighting

based on detected emotion

"""

# Get user's smart home

integrations

integrations = self .db_service.

get_smart_home_integrations

( user_id )

results = [ ]

for integration in integrations:

provider = integration

[ 'provider' ]

# Skip if no access token

if not integration.get

( 'access_token' ) :

continue

# Determine lighting

settings based on emotion

and intensity

settings = self .

_get_lighting_settings

( emotion, intensity )

# Apply settings to the

appropriate provider

if provider ==

'philips_hue' :

result = self .

_adjust_philips_hue

( integration, settings )

elif provider ==

'google_home' :

result = self .

_adjust_google_home

( integration, settings )

else :

result = {

'status' : 'error' ,

'message' :

f 'Unsupported

provider: { provider }

'

}

results.append ( {

'provider' : provider,

'result' : result

} )

return results

def _get_lighting_settings ( self ,

emotion , intensity ) :

"""

Get lighting settings based on

emotion and intensity

"""

# Default settings

settings = {

'brightness' : 100 , # 0-100

'color' : {

'hue' : 0 , # 0-360

'saturation' : 0 # 0-100

}

}

# Adjust settings based on

emotion

if emotion == 'Joy' :

# Warm yellow

settings [ 'color' ] [ 'hue' ] =

45

settings [ 'color' ]

[ 'saturation' ] = 80

settings [ 'brightness' ] = min

( 100 , 70 + ( intensity * 30 ) )

elif emotion == 'Sadness' :

# Soft blue

settings [ 'color' ] [ 'hue' ] =

240

settings [ 'color' ]

[ 'saturation' ] = 40

settings [ 'brightness' ] = max

( 30 , 60 - ( intensity * 30 ) )

elif emotion == 'Anger' :

# Soft red

settings [ 'color' ] [ 'hue' ] = 0

settings [ 'color' ]

[ 'saturation' ] = 60

settings [ 'brightness' ] = min

( 100 , 60 + ( intensity * 40 ) )

elif emotion == 'Fear' :

# Purple

settings [ 'color' ] [ 'hue' ] =

270

settings [ 'color' ]

[ 'saturation' ] = 50

settings [ 'brightness' ] = max

( 30 , 70 - ( intensity * 40 ) )

elif emotion == 'Surprise' :

# Bright cyan

settings [ 'color' ] [ 'hue' ] =

180

settings [ 'color' ]

[ 'saturation' ] = 70

settings [ 'brightness' ] = min

( 100 , 70 + ( intensity * 30 ) )

elif emotion == 'Disgust' :

# Green

settings [ 'color' ] [ 'hue' ] =

120

settings [ 'color' ]

[ 'saturation' ] = 50

settings [ 'brightness' ] = max

( 40 , 70 - ( intensity * 30 ) )

elif emotion == 'Calm' :

# Soft white

settings [ 'color' ] [ 'hue' ] =

30

settings [ 'color' ]

[ 'saturation' ] = 20

settings [ 'brightness' ] = 60

return settings

def _adjust_philips_hue ( self ,

integration , settings ) :

"""

Adjust Philips Hue lights

"""

# In a real implementation, you

would:

# 1. Use the Philips Hue API to

adjust lights

# 2. Handle authentication and

token refresh

# 3. Return success or error

# For now, we'll just return a

placeholder

return {

'status' : 'success' ,

'message' : 'Lighting

adjusted (simulated)' ,

'settings' : settings

}

def _adjust_google_home ( self ,

integration , settings ) :

"""

Adjust Google Home lights

"""

# In a real implementation, you

would:

# 1. Use the Google Home API to

adjust lights

# 2. Handle authentication and

token refresh

# 3. Return success or error

# For now, we'll just return a

placeholder

return {

'status' : 'success' ,

'message' : 'Lighting

adjusted (simulated)' ,

'settings' : settings

}

Fold

### 2. Insight Generation Service
insight_service.py

Apply

Open Folder

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

import os

import uuid

import datetime

import json

from collections import Counter

class InsightService :

def __init__ ( self , database_service )

:

"""

Initialize the insight service

with a database service

"""

self .db_service =

database_service

def generate_insights ( self , user_id )

:

"""

Generate insights for a user

based on their emotion data

"""

# Get emotions for the user

emotions = self .db_service.

get_emotions ( user_id,

time_range = 'month' )

if not emotions:

return {

'status' : 'error' ,

'message' : 'No emotion

data found'

}

# Get recordings for the user

recordings = self .db_service.

get_recordings ( user_id )

# Create a mapping of

recording_id to recording data

recording_map = { r [ 'id' ] : r for

r in recordings }

# Process emotion data

emotion_counts = Counter ( )

emotion_timeline = [ ]

for emotion in emotions:

primary_emotion = emotion

[ 'primary_emotion' ]

recording_id = emotion

[ 'recording_id' ]

# Count emotions

emotion_counts

[ primary_emotion ] += 1

# Add to timeline if we

have the recording

if recording_id in

recording_map:

recording =

recording_map

[ recording_id ]

emotion_timeline.append

( {

'timestamp' :

recording

[ 'created_at' ] ,

'emotion' :

primary_emotion,

'intensity' : emotion

[ 'intensity' ] ,

'confidence' :

emotion

[ 'primary_confidence

' ] ,

'recording_id' :

recording_id

} )

# Sort timeline by timestamp

emotion_timeline.sort

( key = lambda x : x [ 'timestamp' ] )

# Generate insights

insights = [ ]

# Dominant emotion insight

if emotion_counts:

dominant_emotion =

emotion_counts.most_common

( 1 ) [ 0 ] [ 0 ]

insights.append ( self .

_create_insight (

user_id,

f "Your dominant emotion

is { dominant_emotion } " ,

f "Over the past month,

you've experienced

{ dominant_emotion } more

than any other emotion.

" +

self ._get_emotion_tip

( dominant_emotion ) ,

'pattern'

) )

# Emotion pattern insights

if len ( emotion_timeline ) >= 3 :

# Check for repeated

patterns

for i in range ( len

( emotion_timeline ) - 2 ) :

if ( emotion_timeline [ i ]

[ 'emotion' ] ==

emotion_timeline [ i + 2 ]

[ 'emotion' ] and

emotion_timeline [ i ]

[ 'emotion' ] !=

emotion_timeline [ i

+ 1 ] [ 'emotion' ] ) :

pattern_emotion =

emotion_timeline [ i ]

[ 'emotion' ]

trigger_emotion =

emotion_timeline [ i

+ 1 ] [ 'emotion' ]

insights.append

( self .

_create_insight (

user_id,

f "

{ trigger_emotion

} often leads

back to

{ pattern_emotion

} " ,

f "We've noticed

that when you

experience

{ trigger_emotion

} , you often

return to

{ pattern_emotion

} afterward. " +

f "This could

indicate a

recurring

emotional

pattern worth

exploring." ,

'pattern'

) )

break

# Time-based insights

if len ( emotion_timeline ) >= 5 :

# Convert timestamps to

datetime objects

for entry in

emotion_timeline:

entry [ 'datetime' ] =

datetime.datetime.

fromisoformat ( entry

[ 'timestamp' ] )

# Group by hour of day

hour_emotions = { }

for entry in

emotion_timeline:

hour = entry

[ 'datetime' ] .hour

if hour not in

hour_emotions:

hour_emotions [ hour ]

= [ ]

hour_emotions [ hour ] .

append ( entry [ 'emotion' ] )

# Find dominant emotions by

time of day

for period, hours in

[ ( 'morning' , range ( 5 , 12 ) ) ,

( 'afternoon' , range ( 12 ,

18 ) ) ,

( 'eveni

ng' ,

range

( 18 ,

22 ) ) ,

( 'night

' ,

range

( 22 ,

24 ) ) ] :

period_emotions = [ ]

for hour in hours:

if hour in

hour_emotions:

period_emotions.

extend

( hour_emotions

[ hour ] )

if period_emotions:

period_counter =

Counter

( period_emotions )

dominant =

period_counter.

most_common ( 1 ) [ 0 ] [ 0 ]

insights.append

( self .

_create_insight (

user_id,

f "You tend to

feel { dominant }

in the { period }

" ,

f "Based on your

emotional

patterns, you

most often

experience

{ dominant }

during the

{ period } . " +

self .

_get_time_tip

( period,

dominant ) ,

'pattern'

) )

# Save insights to database

for insight in insights:

self .db_service.save_insight

( insight )

return {

'status' : 'success' ,

'insights' : insights

}

def get_insights ( self , user_id ,

unread_only = False ) :

"""

Get insights for a user

"""

insights = self .db_service.

get_insights ( user_id,

unread_only )

return insights

def mark_insight_read ( self ,

insight_id ) :

"""

Mark an insight as read

"""

return self .db_service.

update_insight ( insight_id,

{ 'is_read' : True } )

def _create_insight ( self , user_id ,

title , description , category ) :

"""

Create a new insight

"""

return {

'id' : str ( uuid.uuid4 ( ) ) ,

'user_id' : user_id,

'title' : title,

'description' : description,

'category' : category,

'created_at' : datetime.

datetime.now ( ) .isoformat ( ) ,

'is_read' : False

}

def _get_emotion_tip ( self , emotion ) :

"""

Get a tip based on an emotion

"""

tips = {

'Joy' : "Embrace this

positive emotion and try to

identify what triggers it

so you can recreate these

moments." ,

'Sadness' : "Remember that

sadness is a natural

emotion. Consider

journaling or talking with

someone you trust." ,

'Anger' : "When you feel

anger rising, try deep

breathing exercises or

stepping away from the

situation temporarily." ,

'Fear' : "Grounding

techniques like the

5-4-3-2-1 method can help

manage fear and anxiety." ,

'Surprise' : "Unexpected

events can be opportunities

for growth. Reflect on what

surprised you and why." ,

'Disgust' : "This emotion

often signals a violation

of your values. Reflect on

what triggered this feeling.

" ,

'Calm' : "Notice what brings

you to this balanced state

and try to incorporate more

of these elements into your

routine."

}

return tips.get ( emotion,

"Reflect on what triggers this

emotion and how it affects you.

" )

def _get_time_tip ( self , period ,

emotion ) :

"""

Get a tip based on time of day

and emotion

"""

if period == 'morning' and

emotion in [ 'Sadness' , 'Anger' ,

'Fear' ] :

return "Starting your day

with these emotions can

affect your whole day.

Consider a morning routine

with mindfulness or

exercise."

elif period == 'afternoon' and

emotion in [ 'Sadness' , 'Anger' ,

'Fear' ] :

return "Afternoon slumps

are common. A short walk or

brief meditation might help

shift your emotional state."

elif period == 'evening' and

emotion in [ 'Sadness' , 'Anger' ,

'Fear' ] :

return "Evening emotions

can affect sleep. Try a

calming activity before bed

like reading or gentle

stretching."

elif period == 'night' and

emotion in [ 'Sadness' , 'Anger' ,

'Fear' ] :

return "Nighttime emotions

can disrupt sleep. Consider

a digital sunset an hour

before bed and a relaxing

bedtime routine."

else :

return "Being aware of your

emotional patterns at

different times of day can

help you prepare and

respond effectively."

Fold

### 3. Model Training Script
train_model.py

Apply

Open Folder

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

219

220

221

222

223

224

225

226

227

228

229

import os

import numpy as np

import pandas as pd

import librosa

import tensorflow as tf

from tensorflow.keras.models import

Sequential

from tensorflow.keras.layers import

Dense, Dropout, Flatten, Conv1D,

MaxPooling1D, BatchNormalization

from tensorflow.keras.utils import

to_categorical

from sklearn.model_selection import

train_test_split

from sklearn.preprocessing import

LabelEncoder

import matplotlib.pyplot as plt

import glob

import tqdm

# Define paths

DATA_PATH = os.path.join ( os.path.dirname

( os.path.abspath ( __file__ ) ) , 'data' ,

'training' )

MODEL_PATH = os.path.join ( os.path.

dirname ( os.path.abspath ( __file__ ) ) ,

'models' , 'emotion_model.h5' )

TFLITE_MODEL_PATH = os.path.join ( os.

path.dirname ( os.path.abspath

( __file__ ) ) , 'models' , 'emotion_model.

tflite' )

# Ensure directories exist

os.makedirs ( os.path.dirname

( MODEL_PATH ) , exist_ok = True )

# Define emotions to detect

emotions = [ 'Anger' , 'Disgust' , 'Fear' ,

'Joy' , 'Sadness' , 'Surprise' , 'Calm' ]

def extract_features ( file_path ,

max_pad_len = 174 ) :

"""

Extract MFCC features from audio

file

"""

try :

# Load audio file

y, sr = librosa.load ( file_path,

sr = 22050 )

# Trim silence

y, _ = librosa.effects.trim ( y,

top_db = 25 )

# Extract MFCCs

mfccs = librosa.feature.mfcc

( y = y, sr = sr, n_mfcc = 13 )

# Pad or truncate to fixed

length

pad_width = max_pad_len - mfccs.

shape [ 1 ]

if pad_width > 0 :

mfccs = np.pad ( mfccs,

pad_width = ( ( 0 , 0 ) , ( 0 ,

pad_width ) ) ,

mode = 'constant' )

else :

mfccs = mfccs [ :,

:max_pad_len ]

return mfccs

except Exception as e:

print ( f "Error extracting

features from { file_path } : { e } " )

return None

def load_data ( data_path ) :

"""

Load audio data and extract features

"""

features = [ ]

labels = [ ]

# Check if data path exists

if not os.path.exists ( data_path ) :

print ( f "Data path { data_path }

does not exist. Please download

and prepare the dataset." )

return None , None

# Process each emotion folder

for emotion in emotions:

emotion_path = os.path.join

( data_path, emotion )

# Skip if folder doesn't exist

if not os.path.exists

( emotion_path ) :

print ( f "Emotion folder

{ emotion_path } does not

exist. Skipping." )

continue

# Get all audio files

files = glob.glob ( os.path.join

( emotion_path, "*.wav" ) )

print ( f "Processing { len ( files ) }

files for emotion: { emotion } " )

# Process each file

for file_path in tqdm.tqdm

( files ) :

mfccs = extract_features

( file_path )

if mfccs is not None :

features.append ( mfccs )

labels.append ( emotion )

# Convert to numpy arrays

features = np.array ( features )

# Encode labels

label_encoder = LabelEncoder ( )

labels = label_encoder.fit_transform

( labels )

# Save label encoder mapping

label_mapping = dict ( zip

( label_encoder.classes_,

label_encoder.transform

( label_encoder.classes_ ) ) )

print ( "Label mapping:" ,

label_mapping )

return features, labels

def build_model ( input_shape ,

num_classes ) :

"""

Build CNN model for emotion

classification

"""

model = Sequential ( )

# First convolutional layer

model.add ( Conv1D ( 64 , 3 ,

padding = 'same' , activation = 'relu' ,

input_shape = input_shape ) )

model.add ( BatchNormalization ( ) )

model.add ( MaxPooling1D ( pool_size = 2 ) )

model.add ( Dropout ( 0.2 ) )

# Second convolutional layer

model.add ( Conv1D ( 128 , 3 ,

padding = 'same' , activation = 'relu' ) )

model.add ( BatchNormalization ( ) )

model.add ( MaxPooling1D ( pool_size = 2 ) )

model.add ( Dropout ( 0.2 ) )

# Third convolutional layer

model.add ( Conv1D ( 256 , 3 ,

padding = 'same' , activation = 'relu' ) )

model.add ( BatchNormalization ( ) )

model.add ( MaxPooling1D ( pool_size = 2 ) )

model.add ( Dropout ( 0.2 ) )

# Flatten and dense layers

model.add ( Flatten ( ) )

model.add ( Dense ( 256 ,

activation = 'relu' ) )

model.add ( BatchNormalization ( ) )

model.add ( Dropout ( 0.3 ) )

# Output layer

model.add ( Dense ( num_classes,

activation = 'softmax' ) )

# Compile model

model.compile (

loss = 'categorical_crossentropy' ,

optimizer = 'adam' ,

metrics = [ 'accuracy' ]

)

return model

def train_model ( ) :

"""

Train emotion detection model

"""

# Load data

print ( "Loading and processing

data..." )

features, labels = load_data

( DATA_PATH )

if features is None or labels is

None :

print ( "Failed to load data.

Exiting." )

return

print ( f "Loaded { len ( features ) }

samples." )

# Reshape features for CNN input

features = features.reshape

( features.shape [ 0 ] , features.shape

[ 1 ] , features.shape [ 2 ] , 1 )

# Convert labels to categorical

labels = to_categorical ( labels )

# Split data

X_train, X_test, y_train, y_test =

train_test_split (

features, labels, test_size = 0.

2 , random_state = 42

)

# Build model

print ( "Building model..." )

input_shape = ( X_train.shape [ 1 ] ,

X_train.shape [ 2 ] )

model = build_model ( input_shape, len

( emotions ) )

# Print model summary

model.summary ( )

# Train model

print ( "Training model..." )

history = model.fit (

X_train, y_train,

batch_size = 32 ,

epochs = 50 ,

validation_data = ( X_test,

y_test ) ,

verbose = 1

)

# Evaluate model

print ( "Evaluating model..." )

test_loss, test_accuracy = model.

evaluate ( X_test, y_test, verbose = 0 )

print ( f "Test accuracy:

{ test_accuracy :.4f } " )

# Save model

print ( f "Saving model to

{ MODEL_PATH } ..." )

model.save ( MODEL_PATH )

# Convert to TensorFlow Lite

print ( "Converting to TensorFlow

Lite..." )

converter = tf.lite.TFLiteConverter.

from_keras_model ( model )

tflite_model = converter.convert ( )

# Save TFLite model

with open ( TFLITE_MODEL_PATH, 'wb' )

as f:

f.write ( tflite_model )

print ( f "TensorFlow Lite model saved

to { TFLITE_MODEL_PATH } " )

# Plot training history

plt.figure ( figsize = ( 12 , 4 ) )

plt.subplot ( 1 , 2 , 1 )

plt.plot ( history.history

[ 'accuracy' ] )

plt.plot ( history.history

[ 'val_accuracy' ] )

plt.title ( 'Model Accuracy' )

plt.ylabel ( 'Accuracy' )

plt.xlabel ( 'Epoch' )

plt.legend ( [ 'Train' , 'Validation' ] ,

loc = 'upper left' )

plt.subplot ( 1 , 2 , 2 )

plt.plot ( history.history [ 'loss' ] )

plt.plot ( history.history

[ 'val_loss' ] )

plt.title ( 'Model Loss' )

plt.ylabel ( 'Loss' )

plt.xlabel ( 'Epoch' )

plt.legend ( [ 'Train' , 'Validation' ] ,

loc = 'upper left' )

plt.tight_layout ( )

plt.savefig ( os.path.join ( os.path.

dirname ( MODEL_PATH ) ,

'training_history.png' ) )

plt.close ( )

if __name__ == "__main__" :

train_model ( )

Fold

### 4. Requirements File
requirements.txt

Apply

Open Folder

1

2

3

4

5

6

7

8

9

10

11

12

13

flask==2.0.1

flask-cors==3.0.10

numpy==1.19.5

pandas==1.3.3

matplotlib==3.4.3

librosa==0.8.1

tensorflow==2.6.0

tensorflow-lite==2.6.0

scikit-learn==0.24.2

soundfile==0.10.3.post1

tqdm==4.62.3

requests==2.26.0

pydub==0.25.1

Fold

### 5. README File
README.md

Apply

Open Folder

1

2

3

4

5

6

7

8

9

10

11

12

13

14

# EmoVoice Backend

EmoVoice is an AI-powered emotion

detection system that analyzes voice to

detect emotions and provide insights.

## Features

- Real-time voice emotion analysis

(anger, joy, sadness, etc.)

- Mood timeline tracking with

actionable insights

- Anonymous sharing of emotional

reports with therapists

- Smart home integration (adjust

lighting based on mood)

- On-device processing for privacy

## Project Structure
EmoVoice Backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── train_model.py              # Script to train emotion detection model
├── data/                       # Data directory
│   ├── recordings/             # User recordings
│   ├── reports/                # Generated reports
│   ├── training/               # Training data for model
│   └── emovoice.db             # SQLite database
├── database/                   # Database files
│   └── schema.sql              # Database schema
├── models/                     # Model files
│   └── emotion_model.tflite    # TensorFlow Lite model
└── services/                   # Service modules
├── database_service.py     # Database operations
├── emotion_detection_service.py # Emotion detection
├── insight_service.py      # Insight generation
├── recording_service.py    # Recording management
├── report_service.py       # Report generation
├── smart_home_service.py   # Smart home integration
└── user_service.py         # User management

## Setup and Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Initialize the database:
```bash
python -c "from services.database_service import DatabaseService; DatabaseService('data/emovoice.db').init_database()"
```
4. Train the emotion detection model (optional, pre-trained model included):
```bash
python train_model.py
```
5. Run the application:
```bash
python app.py
```


## API Endpoints

### Health Check
- `GET /api/health` - Check if the API is running

### User Management
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login a user
- `PUT /api/users/<user_id>/preferences` - Update user preferences

### Recording
- `POST /api/recordings` - Upload a new recording
- `GET /api/recordings/<user_id>` - Get recordings for a user
- `GET /api/recordings/<recording_id>/emotion` - Get emotion for a recording

### Reports
- `POST /api/reports` - Generate a new report
- `GET /api/reports/<user_id>` - Get reports for a user
- `POST /api/reports/<report_id>/share` - Share a report
- `GET /api/reports/shared/<token>` - Access a shared report

### Insights
- `GET /api/insights/<user_id>` - Get insights for a user
- `PUT /api/insights/<insight_id>/read` - Mark an insight as read

### Smart Home
- `POST /api/smart-home/integrate` - Register a smart home integration
- `GET /api/smart-home/<user_id>` - Get integrations for a user
- `DELETE /api/smart-home/<integration_id>` - Delete an integration
- `POST /api/smart-home/<user_id>/adjust` - Adjust lighting based on emotion

## Emotion Detection

The emotion detection system uses a Convolutional Neural Network (CNN) trained on MFCC features extracted from audio recordings. The model can detect the following emotions:

- Anger
- Disgust
- Fear
- Joy
- Sadness
- Surprise
- Calm

## Database Schema

The application uses SQLite for data storage with the following tables:

- `users` - User information
- `recordings` - Audio recordings
- `emotions` - Detected emotions
- `reports` - Generated reports
- `report_shares` - Shared reports
- `insights` - Generated insights
- `smart_home_integrations` - Smart home device integrations