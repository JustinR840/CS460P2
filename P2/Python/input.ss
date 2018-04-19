(define (function var)
    (cond ((list? ls) "is a list")
    )
)
(define (function var)
    (car ls)
)
(define (function var)
    (cons (car ls) ls)
)
(define (function var)
    (and 1 1)
)
(define (function var)
    (or 1 1)
)
(define (function var)
    (not (= 1 1))
)
(define (function var)
    (number? 1)
)

(define (function var)
    (list? ls)
)
(define (function var)
    (zero? 0)
)
(define (function var)
    (null? ls)
)
(define (function var)
    (string? "asf")
)
(define (function var)
    (+ 1 1)
)
(define (function var)
    (- 1 1)
)
(define (function var)
    (/ 4 2)
)
(define (function var)
    (* 2 2)
)
(define (function var)
    (= 1 1)
)
(define (function var)
    (> 2 1)
)
(define (function var)
    (< 1 2)
)
(define (function var)
    (>= 2 2)
)
(define (function var)
    (<= 2 2)
)
(define (functio1 var)
    (* 2 2)
)

(define (function2 var)
    (* 1 1)
)
; Rule 24
(define (rule_24_a) (if (> 3 4) 2 3))
(define (rule_24_b) (if (< 3 4) 'true 'false))
(define (rule_24_c) (if (null? '()) 'is_null 'not_null))
(define (rule_24_d) (if (zero? '3) 'is_zero 'not_zero))
; Rule 26
(define (rule_26_a) (car '(a)))
(define (rule_26_b) (cdr '(a)))
(define (rule_26_c) (car '((a)b)))
(define (rule_26_d) (cdr '((a)b)))
(define (rule_26_e) (cadr '((a)b)))
(define (rule_26_f) (cddr '((a)b)))
; Rule 28
(define (rule_28_a) (and))
; Rule 30
(define (rule_30_a) (not (< 4 3)))
(define (rule_30_b) (not (and (= 3 3) (< 2 3))))
; Rule 32
(define (rule_32_a) (symbol? 'a))
; Rule 34
(define (rule_34_a) (zero? 0))
; Rule 36
(define (rule_36_a) (string? "hello, world"))
; Rule 38
(define (rule_38_a) (- 4 2))
; Rule 40
(define (rule_40_a) (* 1 2))
(define (rule_40_b) (*))
; Rule 42
(define (rule_42_a) (= 2 2))
(define (rule_42_b) (=))
; Rule 44
(define (rule_44_a) (< 3 4))
(define (rule_44_b) (<))
; Rule 46
(define (rule_46_a) (<= 3 3))
(define (rule_46_b) (<=))
; Rule 48
(define (rule_48_a) (display "0118999\n"))
(define (rule_48_b) (display 0118999))
;; File: S1.ss
;; Authors: Devin Brown and Ryan Moeller

;; Smallest possible program that compiles
(define (x) x)
;; File: S25.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 25
(define (x) (cond (x x)))
;; File: S27.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 27
(define (x) (cons 0 x))
;; File: S29.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 29
(define (x) (or))
;; File: S31.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 31
(define (x) (number? x))
;; File: S33.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 33
(define (x) (list? x))
;; File: S35.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 35
(define (x) (null? x))
;; File: S37.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 37
(define (x) (+))
;; File: S39.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 39
(define (x) (/ x))
;; File: S41.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 41
(define (x) (modulo x x))
;; File: S43.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 43
(define (x) (>))
;; File: S45.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 45
(define (x) (>=))
;; File: S47.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 47
(define (x) (x))
;; File: S49.ss
;; Authors: Devin Brown and Ryan Moeller

;; Rule 49
(define (x) (newline))
(define (isList a) (if (list? a) a 'param_passed_is_not_list)) ;rule 24 ; rule 33(define (carList a) (car a)) ;rule 26(define (PositiveNumber a) (and (number? a) (<= 0 a))) ;rule 28 (define (NotList a) (not (list? a))) ; rule 30;follow actual  structure, all start with define
(define (isSymbol a) (symbol? a)) ; rule 32(define (isZero a) (zero? a)) ;rule 34(define(isString a) (string? a)) ;rule 36(define(Sub a b) (- a b)) ;rule 38(define(Mult a b) (* a b)) ;rule 40(define(EqaulTo a b) (= a b)) ; rule 42(define(LessThan a b) ( < a b));rule 44(define(LessThanEqual a b) ( <= a b )) ;rule 46(define(DisplayZ a) (display a));rule 48;; File: U25.ss
;; Group U

(define (a)
  (cond (a b)
        (else c)
        )
  )
;; File: U27.ss
;; Group U

(define (a)
  (cons a b)
  )
;; File: U29.ss
;; Group U

(define (a)
  (or b)
  )
;; File: U31.ss
;; Group U

(define (a)
  (number? a)
  )
;; File: U33.ss
;; Group U

(define (a)
  (list? 9)
  )
;; File U35.ss
;; Group U

(define (a)
  (null? 9)
  )
