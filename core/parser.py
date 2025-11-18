from lark import Lark

ROCKWELL_L5X_GRAMMAR = r"""

// --- Start Symbol ---
start : routine

// --- Logic Structure ---
routine     : (rung ";")+              // One or more rungs, each terminated by a semicolon.
rung        : segment+                 // One or more segments (instructions or branches) concatenated sequentially.
?segment    : instruction | branch     // A segment is either a single instruction or a parallel branch.

// Requires at least two segments (parallel paths) separated by commas.
branch      : "[" segment (","? segment?)+ "]"           // Empty segment is allowed

instruction : OPCODE "(" argument? ("," argument?)* ")"  // WARNING! Empty argument is allowed, but will not be parsed correctly (break args index order)

// --- Argument and Expression Components ---
argument    : tag_reference
            | VALUE
            | expression
            | instruction
            | UNDEFINED

// Expression is defined for instructions like CPT (Compute)
expression  : expression "+" expression       -> addition
            | expression "-" expression       -> subtraction
            | expression "*" expression       -> multiplication
            | expression "/" expression       -> division
            | expression "**" expression      -> exponential
            | expression ">" expression       -> greater
            | expression ">=" expression      -> greater_or_equal
            | expression "<" expression       -> less
            | expression "<=" expression      -> less_or_equal
            | expression "=" expression       -> assignment // Use for Assignment inside CPT
            | "(" expression ")"              -> parentheses
            | tag_reference
            | VALUE

// --- RULES FOR TAG STRUCTURE ---
// 1. Tag Reference: Base name followed by zero or more access chains (e.g., Tag, Tag.Member, Tag[1].Bit:Local)
tag_reference   : TAG_NAME access_chain*

// 2. Access Chains: Defines how a tag can be accessed recursively
access_chain    : "." (TAG_NAME | INT)            -> dot_member_access   // .MemberName (e.g., Timer.PRE)
                | ":" (TAG_NAME | INT)            -> colon_module_access // :ModuleName (e.g., Local:3:I)
                | "[" (tag_reference | INT | expression) "]"   -> index_access        // [IndexTag] or [10]

// TOKENIZED TAG NAME: Used for the base name and all member/module names.
TAG_NAME    : CNAME

// OPCODE CNAME is now explicit.
OPCODE      : CNAME

// Standard String token
STRING      : /'[^']*'/

// Custom literal for unquoted configuration values that can contain spaces and hyphens,
// e.g., 'SAFETY GATE', 'EQUIVALENT - ACTIVE HIGH'.
UNQUOTED_LITERAL : /[a-zA-Z0-9_ -%]+/

// Standard Numeric token.
VALUE       : SIGNED_NUMBER | STRING | UNQUOTED_LITERAL

// Placeholder token.
UNDEFINED   : "?"

// --- Common Lark Imports ---
%import common.CNAME
%import common.SIGNED_NUMBER
%import common.INT
%import common.WS
%ignore WS
"""

rockwell_l5x_parser = Lark(ROCKWELL_L5X_GRAMMAR, start="routine")
