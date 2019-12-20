;; Auto-generated. Do not edit!


(when (boundp 'sauvc::lokasi)
  (if (not (find-package "SAUVC"))
    (make-package "SAUVC"))
  (shadow 'lokasi (find-package "SAUVC")))
(unless (find-package "SAUVC::LOKASI")
  (make-package "SAUVC::LOKASI"))

(in-package "ROS")
;;//! \htmlinclude lokasi.msg.html


(defclass sauvc::lokasi
  :super ros::object
  :slots (_xloc ))

(defmethod sauvc::lokasi
  (:init
   (&key
    ((:xloc __xloc) 0)
    )
   (send-super :init)
   (setq _xloc (round __xloc))
   self)
  (:xloc
   (&optional __xloc)
   (if __xloc (setq _xloc __xloc)) _xloc)
  (:serialization-length
   ()
   (+
    ;; uint8 _xloc
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _xloc
       (write-byte _xloc s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _xloc
     (setq _xloc (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get sauvc::lokasi :md5sum-) "82f34519e751e2caec3eadc7bc50234e")
(setf (get sauvc::lokasi :datatype-) "sauvc/lokasi")
(setf (get sauvc::lokasi :definition-)
      "uint8 xloc

")



(provide :sauvc/lokasi "82f34519e751e2caec3eadc7bc50234e")


