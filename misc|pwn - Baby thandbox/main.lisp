(defun echo ()
  (princ "> ")
  (setq cmd (read))
    (case cmd
       ('help (princ "Available commands:")(print "help")(print "flag")(print "quit"))
       ('flag (princ "you wish"))
       ('quit (quit))
       (otherwise (prin1 cmd)))
    (terpri)
    (echo))
(handler-case
  (echo)
  (error (e) (prin1 e)(quit)))
(quit)
