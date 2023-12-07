import cv2
import pyautogui                                                   # Bilgisayar ekranındaki fare ve klavye işlemlerini otomatikleştirmek için kullanılır. 
import imutils                                                     # Pencere yükseeklük ve genişlik ayarlarını yapmak için kullanılan kütüphane
from cvzone.HandTrackingModule import HandDetector                 # El tespiti için kullanılan kütüphane

cap = cv2.VideoCapture(0)                                          # 0 ise pc kamerası 1 ise bağlı olan başka bir kameradan görüntünün gelmesi sağlanmış olur.
detector = HandDetector( detectionCon= 0.6, maxHands=2)            # Güvenilirlik değeri(detectionCon) ne kadar düşükse eli o kadar iyi bulur
                                                                   # maxHands kaç tane el tesiti yapılacağını belirlemek için kullanılır
                                                                   
sw ,sh = pyautogui.size()                                          # Sadece belirlediğimiz çerçeve yüksekliğinde ve genişliğinde mouse kontrülü değil tüm ekranda yapabilmemizi sağlamak için kullanılır
print(sw, sh)                                                      # pyautogui.size(): Bu fonksiyon, ekranın çözünürlüğünü elde etmek için kullanılır 
                                                                   # Ekranın çözünürlüğünü bilmek, piksel koordinatları ile çalışırken doğru konumları belirlemede ve simülasyon işlemlerinde yardımcı olabilir.

while True:
    ret ,frame = cap.read()                                         # VideoCapture nesnesinin read() fonksiyonu, video kaynağından bir kareyi okur. İki değer döndürür: birinci değer ret (return) adlı bir boolean değerdir ve kare başarıyla okunduysa True, 
                                                                    # başarısız olduysa False değerini alır. İkinci değer ise frame adlı bir görüntü dizisidir ve okunan kareyi içerir.  
                                                                                     
    frame = cv2.flip(frame,1)                                       # (frame): Aynalandırılacak olan görüntüdür. 1, görüntünün yatay eksende aynalandırılmasını ifade eder.1
    frame = imutils.resize(frame,640, 480)                          # imutils kütüphanesinin resize fonksiyonu kullanılarak bir görüntünün boyutunu değiştirmek için kullanılır. Yeniden boyutlandırıldıktan sonra ekrana bastırılır.
    fw ,fh = 640, 480                                               # temelde çerçeve genişliği ve yüksekliğidir
    hands ,frame = detector.findHands(frame , flipType= False)      # flipType= False: Bu parametre, görüntünün çevrileceği yönu belirler. False durumunda görüntü çevrilmeyecek demektir.
    
    if hands:
        hand = hands[0] 
        lmList = hand["lmList"]
        x = lmList[8][0]
        y = lmList[8][1]
        cv2.circle(frame ,(x , y), 10, (0,0,255),-1)                # 8 numaralı landmak olan parmak ucundaki dairenin özellikleri
        
        x2 = sw/fw*x                                                # bu işlemler ile fare tam ekrana taşınmmış olur
        y2 = sh/fh*y
        
        pyautogui.moveTo(x2, y2)                                    # parmağımız hareket ettikçe farenin x,y düzlemlerinde hareketi sağlanır
        fingers = detector.fingersUp(hand)                          # parmakların açık ya da kapalı olduğunu anlamak için kullanılır
        print(fingers)
        
        a = fingers[0]                                              # ilk indekse ihtiyaç var yani baş parmak oluyo [0, 1, 1, 1, 1]
        if a==1:                                                    # baş parmak kapalı ise aşağıdaki işlemleri yap:
            pyautogui.click()                                       # fonksiyonu, bilgisayar ekranındaki belirli bir konuma tıklama işlemini gerçekleştirmek için kullanılır. 
            pyautogui.sleep(1)                                      # 1 saniye beklemek için kullanılır
            
    cv2.imshow("image", frame)                                      # görüntünün ekrana gösterilmesi için kullanılır

    if 0xFF & cv2.waitKey(25) == ord('q'):  
         break                                                      # cv2.waitKey(25): Bu fonksiyon, belirli bir süre boyunca bir tuşa basılmasını bekler. Burada, 25 milisaniye boyunca beklenir. Eğer bu süre içinde bir tuşa basılırsa, basılan tuşun ASCII değeri döner.
                                                                    # 0xFF &: Bu ifade, 8 bitlik sınırlamalar nedeniyle Python 2 ve Python 3 arasındaki uyumsuzlukları ele alır.
                                                                    # ord('q'): 'q' tuşunun ASCII değerini döndürür. 
cap.release()                                                       # görüntü serbest bırakılır
    
    
    