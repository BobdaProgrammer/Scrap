
import os
import sys
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_token = None
        self.index = 0

    def getNextToken(self):
        # Skip whitespace
        while self.index < len(self.code) and self.code[self.index].isspace():
            self.index += 1

        if self.index >= len(self.code):
            # End of code
            self.current_token = None
            return
        # Check for comments
        elif self.code[self.index] == '#':
            # Skip single-line comments starting with '#'
            while self.index < len(self.code) and self.code[self.index] != '\n':
                self.index += 1
            if self.index < len(self.code):
                # Skip the newline character
                self.index += 1
            return
        elif self.code[self.index:self.index+10] == "JSexeption":
            self.index+=10
            self.current_token = ("JSexeption")
            self.tokens.append(self.current_token)
        elif self.code[self.index] == "_" and self.code[self.index-1] == "\n":
            self.index+=1
            self.current_token = ("CLOSEjsexeption")
            self.tokens.append(self.current_token)
                # String
        elif self.code[self.index] == '"' or self.code[self.index] == "'" or self.code[self.index] == "`":
            string_delimiter = self.code[self.index]  # Get the string delimiter (either double quote or single quote)
            self.index += 1
            string_value = ""
            while self.index < len(self.code) and self.code[self.index] != string_delimiter:
                # Add each character of the string to the string_value
                string_value += self.code[self.index]
                self.index += 1
            if self.index >= len(self.code):
                # Error: String is not terminated
                raise Exception("String is not terminated")
            self.index += 1  # Skip the closing delimiter
            self.current_token = ("STRING", string_value,string_delimiter)
            self.tokens.append(self.current_token)

        # Check for each token type
        elif self.code[self.index:self.index + 4] == "wait":
            self.index += 4
            self.current_token = ("WAIT", "wait")
            self.tokens.append(self.current_token)
        # Keyword
        elif self.code[self.index:self.index + 3] == "var" or \
                self.code[self.index:self.index + 2] == "if" or \
                self.code[self.index:self.index + 4] == "elif" or \
                self.code[self.index:self.index + 4] == "else" or \
                self.code[self.index:self.index + 2] == "fn" or \
                self.code[self.index:self.index + 3] == "for" or \
                self.code[self.index:self.index + 6] == "return" or \
                self.code[self.index:self.index + 4] == "true" or \
                self.code[self.index:self.index + 5] == "false" or \
                self.code[self.index:self.index + 5] == "while":
            keyword = ""
            while self.index < len(self.code) and (self.code[self.index].isalnum() or self.code[self.index] == '_'):
                keyword += self.code[self.index]
                self.index += 1
            self.current_token = ("KEYWORD", keyword)
            self.tokens.append(self.current_token)
        elif  self.code[self.index:self.index+3] in ("===",">==","<==", "!=="):
            operator = self.code[self.index:self.index + 3]
            self.current_token = ("OPERATOR", operator)
            self.tokens.append(self.current_token)
            self.index += 3
                # Operator

        elif  self.code[self.index:self.index + 2] in ("==", "!=", ">=", "<=","+=","-=","++", "--", "=>", "=<","&&","||","*=","/="):
            operator = self.code[self.index:self.index + 2]
            self.current_token = ("OPERATOR", operator)
            self.tokens.append(self.current_token)
            self.index += 2
                # Operator
        elif self.code[self.index] in "+-*/%=><":
            operator = self.code[self.index]
            self.current_token = ("OPERATOR", operator)
            self.tokens.append(self.current_token)
            self.index += 1
        # Delimiter
        elif self.code[self.index] in "(){},;[].:!_":
            delimiter = self.code[self.index]
            self.index += 1
            self.current_token = ("DELIMITER", delimiter)
            self.tokens.append(self.current_token)


        # Identifier
        elif self.code[self.index].isalpha():
            identifier = ""
            while self.index < len(self.code) and (self.code[self.index].isalnum() or self.code[self.index] == '_'):
                identifier += self.code[self.index]
                self.index += 1
            self.current_token = ("IDENTIFIER", identifier)
            self.tokens.append(self.current_token)

        # Number
        elif self.code[self.index].isdigit():
            number = ""
            while self.index < len(self.code) and self.code[self.index].isdigit():
                number += self.code[self.index]
                self.index += 1
            self.current_token = ("NUMBER", number)
            self.tokens.append(self.current_token)

        else:
            if "\n"in self.code[self.index] == False:
                # Unrecognized token or error handling
                print("Unrecognized token:", "'"+self.code[self.index]+"'")
                self.current_token = None

    def tokenize(self):
        self.getNextToken()  # Call getNextToken() initially

        while self.current_token is not None:
            self.getNextToken()

        return self.tokens


    
def parse_program(tokens):
        JScode = []
        InFor = False
        InFn = False
        InWait = False
        ForVar = ""
        ForVarNum = 0
        tokenCount = 0
        SkipFor = False
        requirement = 0
        meeter = 0
        JSexpt = False
        for index,token in enumerate(tokens):
            if SkipFor == True:
                meeter += 1
                if meeter < requirement:
                    continue
                else:
                    requirement = 0
                    meeter = 0
                    SkipFor = False
            if JSexpt == True:
                if token[0] == "STRING":
                    JScode.append(token[2]+token[1]+token[2])
                elif token[1] == "}":
                    JScode.append("}")
                    JScode.append("\n")
                elif token[1] == "{":
                    JScode.append("{")
                    JScode.append("\n")
                elif token == "CLOSEjsexeption":
                    JSexpt = False
                    continue
                else:
                    JScode.append(token[1]+" ")
                continue
            token1 = index
            token = tokens[index]
            if token == "JSexeption":
                JSexpt = True
                continue
            elif "".join([t[1] for t in tokens[token1:token1+4]]) == "Clearlog();":
                JScode.append("console.clear();")
                SkipFor = True
                requirement = 4
            elif token[0] == "STRING":
                JScode.append(token[2]+token[1]+token[2])
            elif token[1] == ";":
                JScode.append(";")
                if InFor == False:
                    JScode.append("\n")
            elif token[1] == "ReadFile":
                JScode.append("await"+" ")
                JScode.append("ReadFile")
            elif token[0] == "WAIT":
                tokenCount = 0 
                tokenCount = token1+1
                while tokens[tokenCount][1] != ";":
                    tokenCount+=1
                JScode.append("await new Promise(resolve => setTimeout(resolve, " + "".join([t[1] for t in tokens[token1+2:tokenCount-1]])+"))")
                SkipFor = True
                requirement = len(" ".join([t[1] for t in tokens[token1+6:tokenCount-1]]))+4
                InWait = True
            elif token[1] == "prompt":
                if InFn == False:
                    JScode.append("await ")
                    JScode.append(token[1]+" ")
                else:
                    JScode.append(token[1]+" ")
            elif token[1] == "for":
                JScode.append("for")
                JScode.append("(")
                tokenCount = token1+1
                while tokens[tokenCount][1] != "{":
                    tokenCount+=1
                if "in" in tokens[token1+3][1]:
                    ForVar = tokens[token1+2][1]
                    ForMain = "".join([t[1] for t in tokens[token1+4:tokenCount]])
                    JScode.append(ForVar+" ")
                    JScode.append("in ")
                    JScode.append(ForMain)
                    ForVar = ""
                    requirement = len([t[1] for t in tokens[token1:tokenCount]])
                    InFor  = False
                    ForVarNum = 0
                    tokenCount = 0
                    SkipFor = True
                else:
                    ForVar = tokens[token1+2][1]
                    ForVarNum = tokens[token1+4][1]
                    ForAmount = " ".join([t[1] for t in tokens[token1+6:tokenCount-1]])
                    JScode.append("var ")
                    JScode.append(ForVar+" ")
                    JScode.append("= ")
                    JScode.append(ForVarNum)
                    JScode.append(";")
                    JScode.append(ForVar+" ")
                    JScode.append("<=")
                    JScode.append(ForAmount)
                    JScode.append(";")
                    JScode.append(ForVar)
                    JScode.append("++")
                    JScode.append(")")
                    ForVar = ""
                    requirement = len([t[1] for t in tokens[token1+1:tokenCount]])+1
                    InFor  = False
                    ForVarNum = 0
                    tokenCount = 0
                    SkipFor = True
            elif token[1] == "var":
                JScode.append("let"+" ")
            elif token[1] == "break":
                JScode.append("break")
            elif token[1] == "ReadKey":
                JScode.append("await ")
                JScode.append("ReadKey")
            elif token[1] == "GetKey":
                JScode.append("await ")
                JScode.append("GetKey")
            elif token[1] == "log":
                JScode.append("console.log")
            elif token[0] == "IDENTIFIER":
                JScode.append(token[1]+" ")
            elif token[0] == "NUMBER":
                    if InWait == False:
                        JScode.append(token[1]+" ")
            elif token[1] == "fn":
                JScode.append("function"+" ")
                InFn = True
            elif token[1] == "(":
                if InWait == False:
                    JScode.append("(")
            elif token[1] == ")":
                if InWait == True:
                    InWait = False
                else:
                    JScode.append(")")
            elif token[1] == "{":
                if InFn == True:
                    InFn = False
                JScode.append("{")
                if tokens[token1+1][0] != "DELIMITER":
                    JScode.append("\n")
            elif token[1] == "}":
                JScode.append("}")
                JScode.append("\n")
            elif token[1] == "[":
                JScode.append(token[1]+" ")
            elif token[1] == "]":
                JScode.append(token[1]+" ")
            elif token[1] == ".":
                JScode.append(token[1])
            elif token[1] == ",":
                JScode.append(token[1]+" ")
            elif token[0] == "OPERATOR":
                JScode.append(token[1]+" ")
            elif token[0] == "KEYWORD" and token[1] != "elif" and token != "for":
                JScode.append(token[1]+" ")
            elif token[1] == "elif":
                JScode.append("else if ")
            elif token[0] == "DELIMITER":
                JScode.append(token[1])
            else:
                JScode.append("Unknown")

        return JScode


def run_js_code(js_code):
    # Create a temporary file path
    temp_file = "temp.js"

    try:
        # Write the JS code to the temporary file
        with open(temp_file, "w") as file:
            file.write(js_code)

        # Run the Node.js command to execute the temporary file

        result = os.system("node" + " "+ temp_file)


    finally:
        #Delete the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
def Help():
    print('''
    scrap <filename>                                    runs scrap file

    Syntax:
    log(<text>);                                        prints to console
    if(<condition> == true)                             checks if a condition is true
    for(<variable name> = <number> to <end number>)
    while(<condition>)                                  will run a loop until a condition is false
    fn <function name>(<input variables>)               creates a function
    {}                                                  used after if statments, functions, for loops and while loops and used to store the content in them
    prompt(<prompt message>);                           asks the user a question and gets there input
    var <variable name> = <value>;                      creates variable
    +=                                                  used to add numbers or variables
    -=                                                  used to subtract numbers or variables
    >=                                                  used to check if numbers or variables are larger thann another
    <=                                                  used to check if numbers or variables are smaller than eachother''')
def complete():
        if len(sys.argv) > 1:
            Develop = False
            file_path = sys.argv[1]
            if(len(sys.argv))>2:
                Develop = True
            if file_path == "help" or file_path == "Help":
                Help()
            else:
                with open(file_path, "r") as file:
                    code = file.read()
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                js_code = ''.join(parse_program(tokens))
                # Add the import statement and async function to handle prompt
                # Add the import statement and async function to handle prompt
                prompt_code = '''
                const fs = require("fs");
                const keypress = require("keypress");
const readline = require('readline');
const tty = require('tty');
const { exec } = require('child_process');
const { spawn } = require('child_process');
function command(commandToRun){
// Replace 'your_command_here' with the actual command you want to run

exec(commandToRun, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Command execution failed: ${stderr}`);
    return;
  }
  console.log(`${stdout}`);
});
}
async function ReadKey() {
  return new Promise((resolve) => {
    function keyPressListener(str, key) {
      if (key) {
        process.stdin.removeListener('keypress', keyPressListener); // Remove the event listener

        // If the key is a printable character, return it as a string
        if (str && str.length === 1) {
          resolve(str);
        } else {
          // If the key is a special key (e.g., arrow keys, function keys), return it as an object
          resolve({
            name: key.name,
            ctrl: key.ctrl,
            meta: key.meta,
            shift: key.shift,
          });
        }
      }
    }

    // Set raw mode to capture individual keypress events
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.isTTY) {
      process.stdin.setRawMode(true);
    }

    // Start listening for keypress events
    process.stdin.resume();

    // Listen for keypress events
    process.stdin.on('keypress', keyPressListener);
  });
}
async function GetKey() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  return new Promise((resolve) => {
    let timer;
    const onKeyPress = (chunk, key) => {
      clearTimeout(timer);
      rl.close();
      if (key.name !== undefined) {
        resolve(key.name);
        process.stdin.removeAllListeners('keypress');
      }
    };

    process.stdin.on('keypress', onKeyPress);

    // Enable raw mode to capture single keypress events
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.isTTY) {
      process.stdin.setRawMode(true);
    }

    // Set a timer to stop listening after the specified timeout
    timer = setTimeout(() => {
      process.stdin.removeListener('keypress', onKeyPress);
      rl.close();
      resolve(null); // Resolve with null when timeout occurs
      process.stdin.removeAllListeners('keypress');
    }, 0);
  });
}
function RandomInt(min, max) {
  // The Math.random() method returns a random floating-point number between 0 and 1 (exclusive of 1).
  // To get a random number within a range, we multiply the random value by (max - min + 1)
  // and add the minimum value.
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


                function ReadFile(path) {
                    return new Promise((resolve, reject) => {
                        fs.readFile(path, 'utf8', (err, data) => {
                            if (err) {
                                reject(err);
                            } else {
                                resolve(data);
                            }
                        });
                    });
                }

                async function prompt(promptMessage) {
                    return new Promise((resolve, reject) => {
                        const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
                        rl.question(promptMessage, (answer) => {
                            rl.close();
                            resolve(answer);
                        });
                    });
                }

                async function run_js_code() {
                    try {
                '''
                js_code = js_code
                js_code += '''
                    } catch (error) {
                        console.error("Error:", error);
                    }
                }

                run_js_code();
                '''
                # Combine the code
                combined_code = prompt_code + js_code
                if(Develop == True):
                    print(combined_code)
                
                # Run the JS code
                run_js_code(combined_code)
        else:
            Help()
complete()