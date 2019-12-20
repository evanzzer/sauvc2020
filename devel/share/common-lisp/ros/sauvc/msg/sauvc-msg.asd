
(cl:in-package :asdf)

(defsystem "sauvc-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "lokasi" :depends-on ("_package_lokasi"))
    (:file "_package_lokasi" :depends-on ("_package"))
  ))