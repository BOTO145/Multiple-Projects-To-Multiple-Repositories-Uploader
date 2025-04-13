import google.generativeai as genai

def generate_readme(api_key, arduino_code):
    """Generates a README for an Arduino code snippet."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-pro-exp')  # Or gemini-pro if needed

    prompt = f"""
    You are an expert at creating README files for Arduino projects.
    Given the following Arduino code, create a comprehensive README that includes:

    1.  A clear and concise project title.
    2.  A brief description of what the code does.
    3.  A list of required hardware components.
    4.  Wiring instructions or a wiring diagram (if applicable).
    5.  Instructions on how to upload the code to an Arduino board.
    6.  Any relevant notes or explanations about the code's functionality.
    7.  Example usage.

    Arduino Code:
    ```cpp
    {arduino_code}
    ```

    README:
    """

    response = model.generate_content(prompt)
    return response.text

def main():
    api_key = ""  # Replace with your API key

    arduino_code = """
    #include <Servo.h>
    Servo rotate;
    Servo arm1;
    Servo arm2;
    Servo grabber;
    int pos = 0;

    void setup() {
    rotate.attach(3);
    arm1.attach(5);
    arm2.attach(6);
    grabber.attach(9);

    }

    void loop() {
      pos = 90;
      rotate.write(pos);
      arm1.write(pos);
      arm2.write(pos);
      grabber.write(pos);  // tell servo to go to position in variable 'pos'
    }

    """

    readme = generate_readme(api_key, arduino_code)
    if readme:
        print(readme)

if __name__ == "__main__":
    main()
