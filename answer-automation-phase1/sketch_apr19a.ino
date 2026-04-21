#include <Keyboard.h>
#include <avr/pgmspace.h>

const int touchPin = 2;

// ✅ STORED IN FLASH (NOT RAM)
const char code[] PROGMEM =
"import java.util.*;\n"
"\n"
"public class BestFirstSearch {\n"
"\n"
"    static void bestFirstSearch(Map<Character, List<Character>> graph, char start, char goal, Map<Character, Integer> h) {\n"
"        Set<Character> visited = new HashSet<>();\n"
"\n"
"        PriorityQueue<Character> pq = new PriorityQueue<Character>(new Comparator<Character>() {\n"
"            public int compare(Character a, Character b) {\n"
"                return h.get(a) - h.get(b);\n"
"            }\n"
"        });\n"
"\n"
"        pq.add(start);\n"
"\n"
"        while (!pq.isEmpty()) {\n"
"            char node = pq.poll();\n"
"\n"
"            if (node == goal) {\n"
"                System.out.println(\"Reached goal: \" + node);\n"
"                return;\n"
"            }\n"
"\n"
"            if (!visited.contains(node)) {\n"
"                System.out.print(node + \" \");\n"
"                visited.add(node);\n"
"\n"
"                for (char neighbor : graph.get(node)) {\n"
"                    if (!visited.contains(neighbor)) {\n"
"                        pq.add(neighbor);\n"
"                    }\n"
"                }\n"
"            }\n"
"        }\n"
"    }\n"
"\n"
"    public static void main(String[] args) {\n"
"\n"
"        Map<Character, List<Character>> graph = new HashMap<Character, List<Character>>();\n"
"\n"
"        graph.put('A', Arrays.asList('B', 'C'));\n"
"        graph.put('B', Arrays.asList('D', 'E'));\n"
"        graph.put('C', Arrays.asList('F'));\n"
"        graph.put('D', new ArrayList<Character>());\n"
"        graph.put('E', new ArrayList<Character>());\n"
"        graph.put('F', new ArrayList<Character>());\n"
"\n"
"        Map<Character, Integer> h = new HashMap<Character, Integer>();\n"
"        h.put('A', 5);\n"
"        h.put('B', 3);\n"
"        h.put('C', 4);\n"
"        h.put('D', 1);\n"
"        h.put('E', 2);\n"
"        h.put('F', 0);\n"
"\n"
"        bestFirstSearch(graph, 'A', 'F', h);\n"
"    }\n"
"}\n";


// 🔥 TYPE FROM FLASH
void typeSlow_P(const char* text) {
  char c;

  while ((c = pgm_read_byte(text++))) {

    if (c == '\n') {
      Keyboard.press(KEY_RETURN);
      delay(10);
      Keyboard.release(KEY_RETURN);
      delay(120);
    } 
    else {
      Keyboard.press(c);
      delay(10);
      Keyboard.release(c);
      delay(110);
    }
  }
}

void setup() {
  pinMode(touchPin, INPUT_PULLUP);
  Keyboard.begin();

  delay(5000); // time to open editor
}

void loop() {
  if (digitalRead(touchPin) == LOW) {
    delay(200);

    Keyboard.releaseAll(); // safety reset
    delay(200);

    typeSlow_P(code);

    delay(8000); // prevent retrigger
  }
}