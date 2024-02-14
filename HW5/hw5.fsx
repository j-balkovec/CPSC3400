//{
//  @course: CPSC 3400
//  @author: Jakob Balkovec
//  @instructor: B. Diaz Acosta
//
//  @file: hw5.fsx
//  @due: Mon, Feb 21st [22:00]
//
//  @submission_dir: /home/fac/bdiazacosta/submit/cpsc3400/hw5_submit
//  @file: /home/fac/bdiazacosta/cpsc3400/hw5/hw5.fsx
//
//  @brief
//
//  This file contains three F# exercises for homework 5:
//  - simplifies algebraic expressions based on a custom discriminated union type. 
//  - It removes divide and power operations while introducing a second variable y. 
//  - The expr is represented using the Expression type, which includes variables x and y, constants, 
//    negation, addition, subtraction, and multiplication. The function is designed to simplify expressions 
//    according to specified rules and is accompanied by a helper function exprToString for converting 
//    expressions to a readable string format.
//}

// @name: HW5
// @breif: Made for unit_tests
//namespace HW5

open System
open Microsoft.FSharp.Core

// @name: ExpressionSimplification
// @brief: Packed in a module for clarity
module ExpressionSimplification =

    // @name: Expression
    // @brief: Represents algebraic expressions involving variables, constants, and operations
    type Expression =
        | X
        | Y
        | Const of float
        | Neg of Expression
        | Add of Expression * Expression
        | Sub of Expression * Expression
        | Mul of Expression * Expression

    // @name: exprToString
    // @return: [string] -> strign representation of an expresion
    // @param: expr [Expression]
    // @constraints: type of arg has to match Expresssion else it throws a System Error
    let exprToString expr =
        let rec recExprStr parens expr =
            let lParen = if parens then "(" else ""
            let rParen = if parens then ")" else ""
            match expr with
            | X -> "x"
            | Y -> "y"
            | Const n -> n.ToString()
            | Neg e -> lParen + "-" + recExprStr true e + rParen
            | Add (e1, e2) -> lParen + recExprStr true e1 + "+" + recExprStr true e2 + rParen
            | Sub (e1, e2) -> lParen + recExprStr true e1 + "-" + recExprStr true e2 + rParen
            | Mul (e1, e2) -> lParen + recExprStr true e1 + "*" + recExprStr true e2 + rParen
        recExprStr false expr

    // @name: simplify
    // @return: [Expression] the simplified expression
    // @param: expr [Expression]
    // @pre: The input expression must be a valid mathematical expression.
    // @post: The returned expression is simplified according to the rules defined.
    //
    // @note: This function recursively simplifies the input expression by performing
    //        algebraic simplifications such as combining constants, removing zeros,
    //        and merging like terms in addition, subtraction, and multiplication expressions.
    // @bug:
    //
    // ***[t16]*** Correct: 0          Actual: x-x -> sub
    // expr: Sub (Mul (Const 1.0, X), Add (X, Const 0.0))
    // >>> Mul(1, X) -> X
    // >>> Add(X, O) -> X
    // >>> 
    // >>> Sub (X, X)
    let rec simplify (expr: Expression) =
        match expr with
        | Const _ -> expr
        | X -> expr
        | Y -> expr
        
        | Neg (Neg e) -> simplify e
        | Neg (Const e) when e < 0.0 -> Const (-e) |> simplify
        | Neg e -> Neg (simplify e)
        | Neg (Const number) -> Const (-number) |> simplify 
        
        | Add (expr1, expr2) ->
            let simplifiedExpr1 = simplify expr1
            let simplifiedExpr2 = simplify expr2
            match (simplifiedExpr1, simplifiedExpr2) with
            | (_, Const 0.0) -> simplifiedExpr1
            | (Const 0.0, _) -> simplifiedExpr2
            | (Const num1, Const num2) -> Const (num1 + num2) |> simplify 
            | _ -> Add (simplifiedExpr1, simplifiedExpr2)
        
        | Sub (expr1, expr2) ->
            let simplifiedExpr1 = simplify expr1
            let simplifiedExpr2 = simplify expr2
            if simplifiedExpr1 = simplifiedExpr2 then
                Const 0.0
            else
            match (simplifiedExpr1, simplifiedExpr2) with
            | (_, Const 0.0) -> simplifiedExpr1
            | (Const 0.0, _) -> simplify (Neg(simplifiedExpr2))
            | (Const num1, Const num2) -> Const (num1 - num2) |> simplify
            | _ -> Sub (simplifiedExpr1, simplifiedExpr2)

        | Mul (Const 0.0, _) -> Const 0.0
        | Mul (_, Const 0.0) -> Const 0.0
        | Mul (Const 1.0, e) -> simplify e
        | Mul (e, Const 1.0) -> simplify e
        | Mul (expr1, expr2) ->
            let simplifiedExpr1 = simplify expr1
            let simplifiedExpr2 = simplify expr2
            match (simplifiedExpr1, simplifiedExpr2) with
            | (Const num1, Const num2) -> Const (num1 * num2) |> simplify
            | _ -> Mul (simplifiedExpr1, simplifiedExpr2)

        | _ -> failwith "[ERROR]: Expression not recognised"

    printfn "---Provided Tests---"
    let t1 = Add (Const 9.0, Const 4.0)
    let t2 = Sub (Const 10.0, Const 3.5)
    let t3 = Mul (Const 6.0, Const 7.0)
    let t4 = Neg (Const 0.3)
    let t5 = Neg (Const -9.0)
    let t6 = Add (X, Const 0.0)
    let t7 = Add (Const 0.0, Y)
    let t8 = Sub (X, Const 0.0)
    let t9 = Sub (Const 0.0, Y)
    let t10 = Sub (Y, Y)
    let t11 = Mul (X, Const 0.0)
    let t12 = Mul (Const 0.0, Y)
    let t13 = Mul (X, Const 1.0)
    let t14 = Mul (Const 1.0, Y)
    let t15 = Neg (Neg X)                                                                             
    let t16 = Sub (Mul (Const 1.0, X), Add (X, Const 0.0))                                            
    let t17 = Add (Sub (Const 3.0, Const 8.0), Mul (Const 7.0, Const 3.0))                            
    let t18 = Sub (Sub (Add (Y, Const 3.0), Add (Y, Const 3.0)), Add (Const 0.0, Add (Y, Const 3.0))) 
    let t19 = Sub (Const 0.0, Neg (Mul (Const 1.0, X)))                                               
    let t20 = Mul (Add (X, Const 2.0), Neg (Sub (Mul (Const 2.0, Y), Const 5.0)))

    printfn "t1 Correct: 13\t\tActual: %s" (exprToString (simplify t1))
    printfn "t2 Correct: 6.5\t\tActual: %s" (exprToString (simplify t2))
    printfn "t3 Correct: 42\t\tActual: %s" (exprToString (simplify t3))
    printfn "t4 Correct: -0.3\tActual: %s" (exprToString (simplify t4))
    printfn "t5 Correct: 9\t\tActual: %s" (exprToString (simplify t5))
    printfn "t6 Correct: x\t\tActual: %s" (exprToString (simplify t6))
    printfn "t7 Correct: y\t\tActual: %s" (exprToString (simplify t7))
    printfn "t8 Correct: x\t\tActual: %s" (exprToString (simplify t8))
    printfn "t9 Correct: -y\t\tActual: %s" (exprToString (simplify t9))
    printfn "t10 Correct: 0\t\tActual: %s" (exprToString (simplify t10))
    printfn "t11 Correct: 0\t\tActual: %s" (exprToString (simplify t11))
    printfn "t12 Correct: 0\t\tActual: %s" (exprToString (simplify t12))
    printfn "t13 Correct: x\t\tActual: %s" (exprToString (simplify t13))
    printfn "t14 Correct: y\t\tActual: %s" (exprToString (simplify t14))
    printfn "t15 Correct: x\t\tActual: %s" (exprToString (simplify t15))

    printfn "t16 Correct: 0\t\tActual: %s" (exprToString (simplify t16))
    printfn "t17 Correct: 16\t\tActual: %s" (exprToString (simplify t17))
    printfn "t18 Correct: -(y+3)\tActual: %s" (exprToString (simplify t18))
    printfn "t19 Correct: x\t\tActual: %s" (exprToString (simplify t19))
    printfn "t20 Correct: (x+2)*(-((2*y)-5)) Actual: %s" (exprToString (simplify t20))
