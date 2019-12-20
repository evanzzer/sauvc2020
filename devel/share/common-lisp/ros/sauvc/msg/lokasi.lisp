; Auto-generated. Do not edit!


(cl:in-package sauvc-msg)


;//! \htmlinclude lokasi.msg.html

(cl:defclass <lokasi> (roslisp-msg-protocol:ros-message)
  ((xloc
    :reader xloc
    :initarg :xloc
    :type cl:fixnum
    :initform 0))
)

(cl:defclass lokasi (<lokasi>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <lokasi>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'lokasi)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sauvc-msg:<lokasi> is deprecated: use sauvc-msg:lokasi instead.")))

(cl:ensure-generic-function 'xloc-val :lambda-list '(m))
(cl:defmethod xloc-val ((m <lokasi>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sauvc-msg:xloc-val is deprecated.  Use sauvc-msg:xloc instead.")
  (xloc m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <lokasi>) ostream)
  "Serializes a message object of type '<lokasi>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'xloc)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <lokasi>) istream)
  "Deserializes a message object of type '<lokasi>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'xloc)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<lokasi>)))
  "Returns string type for a message object of type '<lokasi>"
  "sauvc/lokasi")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'lokasi)))
  "Returns string type for a message object of type 'lokasi"
  "sauvc/lokasi")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<lokasi>)))
  "Returns md5sum for a message object of type '<lokasi>"
  "82f34519e751e2caec3eadc7bc50234e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'lokasi)))
  "Returns md5sum for a message object of type 'lokasi"
  "82f34519e751e2caec3eadc7bc50234e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<lokasi>)))
  "Returns full string definition for message of type '<lokasi>"
  (cl:format cl:nil "uint8 xloc~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'lokasi)))
  "Returns full string definition for message of type 'lokasi"
  (cl:format cl:nil "uint8 xloc~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <lokasi>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <lokasi>))
  "Converts a ROS message object to a list"
  (cl:list 'lokasi
    (cl:cons ':xloc (xloc msg))
))
