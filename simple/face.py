import face_recognition
image1 = face_recognition.load_image_file("C:\\Users\\sloan\\Pictures\\imag\\a.png");
image2 = face_recognition.load_image_file("C:\\Users\\sloan\\Pictures\\imag\\b.png");
image3 = face_recognition.load_image_file("C:\\Users\\sloan\\Pictures\\imag\\c.png");
encoding1 = face_recognition.face_encodings(image1)[0]
encoding2 = face_recognition.face_encodings(image2)[0]
encoding3 = face_recognition.face_encodings(image3)[0]
results = face_recognition.compare_faces([encoding1,encoding3], encoding2)
print('results:'+str(results))