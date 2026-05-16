# Gemini API Quick Reference

Source: https://ai.google.dev/gemini-api/docs
Generated: 2026-05-06

### Gemini API quickstart
*Source: /quickstart*

> [!IMPORTANT]
> We have updated our [Terms of Service](https://ai.google.dev/gemini-api/terms).

This quickstart shows you how to install our [libraries](https://ai.google.dev/gemini-api/docs/libraries)
and make your first Gemini API request.

## Before you begin

Using the Gemini API requires an API key, you can create one for free to get started.

[Create a Gemini API Key](https://aistudio.google.com/app/apikey)

## Install the Google GenAI SDK

### Python

Using [Python 3.9+](https://www.python.org/downloads/), install the
[`google-genai` package](https://pypi.org/project/google-genai/)
using the following
[pip command](https://packaging.python.org/en/latest/tutorials/installing-packages/):

    pip install -q -U google-genai

### JavaScript

Using [Node.js v18+](https://nodejs.org/en/download/package-manager),
install the
[Google Gen AI SDK for TypeScript and JavaScript](https://www.npmjs.com/package/@google/genai)
using the following
[npm command](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm):

    npm install @google/genai

### Go

Install
[google.golang.org/genai](https://pkg.go.dev/google.golang.org/genai) in
your module directory using the [go get command](https://go.dev/doc/code):

    go get google.golang.org/genai

### Java

If you're using Maven, you can install
[google-genai](https://github.com/googleapis/java-genai) by adding the
following to your dependencies:

    <dependencies>
      <dependency>
        <groupId>com.google.genai</groupId>
        <artifactId>google-genai</artifactId>
        <version>1.0.0</version>
      </dependency>
    </dependencies>

### C#

Install
[googleapis/go-genai](https://googleapis.github.io/dotnet-genai/) in
your module directory using the [dotnet add command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-add)

    dotnet add package Google.GenAI

### Apps Script

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Models
*Source: /models*

> [!IMPORTANT]
> We have updated our [Terms of Service](https://ai.google.dev/gemini-api/terms).

*** ** * ** ***

## Gemini 3

[### Gemini 3.1 Pro
Advanced intelligence, complex problem-solving skills, and powerful agentic and vibe coding capabilities.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) [### Gemini 3 Flash
Frontier-class performance rivaling larger models at a fraction of the cost.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview) [### Gemini 3.1 Flash-Lite
Frontier-class performance rivaling larger models at a fraction of the cost.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-preview) [### Nano Banana 2
Powerful, high-efficiency image generation and editing, optimized for speed and high-volume use cases.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image-preview) [### Nano Banana Pro
State-of-the-art image generation and editing models for highly contextual native image creation.
Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview) [### Gemini 3.1 Flash Live
High-quality, low-latency Live API model for real-time dialogue and voice-first AI applications.
New Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview) [### Gemini 3.1 Flash TTS
Powerful, low-latency speech generation.
New Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview)

> [!WARNING]
> **Warning:** Gemini 3 Pro Preview is [deprecated](https://ai.google.dev/gemini-api/docs/deprecations) and has been shut down March 9, 2026. Migrate to [Gemini 3.1 Pro Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) to avoid service disruption.

*** ** * ** ***

## Gemini 2.5 Flash

### [Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash)

Our best price-performance model for low-latency, high-volume tasks that require reasoning.

### [Nano Banana](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image)

State-of-the-art native image generation and editing designed for fast, creative workflows.

### [Gemini 2.5 Flash Live Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025)

Optimized for real-time conversational agents with sub-second native audio streaming.

### [Gemini 2.5 Flash TTS Preview](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-preview-tts)

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Text generation
*Source: /text-generation*

The Gemini API can generate text output from text, images, video, and audio
inputs.

Here's a basic example:

### Python

    from google import genai

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="How does AI work?"
    )
    print(response.text)

### JavaScript

    import { GoogleGenAI } from "@google/genai";

    const ai = new GoogleGenAI({});

    async function main() {
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: "How does AI work?",
      });
      console.log(response.text);
    }

    await main();

### Go

    package main

    import (
      "context"
      "fmt"
      "os"
      "google.golang.org/genai"
    )

    func main() {

      ctx := context.Background()
      client, err := genai.NewClient(ctx, nil)
      if err != nil {
          log.Fatal(err)
      }

      result, _ := client.Models.GenerateContent(
          ctx,
          "gemini-3-flash-preview",
          genai.Text("Explain how AI works in a few words"),
          nil,
      )

      fmt.Println(result.Text())
    }

### Java

    import com.google.genai.Client;
    import com.google.genai.types.GenerateContentResponse;

    public class GenerateContentWithTextInput {
      public static void main(String[] args) {

        Client client = new Client();

        GenerateContentResponse response =
            client.models.generateContent("gemini-3-flash-preview", "How does AI work?", null);

        System.out.println(response.text());
      }
    }

### REST

    curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "contents": [
          {
            "parts": [
              {
                "text": "How does AI work?"
              }
            ]
          }
        ]
      }'

### Apps Script

    // See https://developers.google.com/apps-script/guides/properties
    // for instructions on how to set the API key.
    const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');

    function main() {
      const payload = {
        contents: [
          {
            parts: [
              { text: 'How AI does work?' },
            ],
          },
        ],
      };

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Function calling with the Gemini API
*Source: /function-calling*

Function calling lets you connect models to external tools and APIs.
Instead of generating text responses, the model determines when to call specific
functions and provides the necessary parameters to execute real-world actions.
This allows the model to act as a bridge between natural language and real-world
actions and data. Function calling has 3 primary use cases:

- **Augment Knowledge:** Access information from external sources like databases, APIs, and knowledge bases.
- **Extend Capabilities:** Use external tools to perform computations and extend the limitations of the model, such as using a calculator or creating charts.
- **Take Actions:** Interact with external systems using APIs, such as scheduling appointments, creating invoices, sending emails, or controlling smart home devices.

> [!NOTE]
> **Important:** Gemini 3 model APIs now generate a unique `id` for every function call. If you are manually constructing the conversation history or using the REST API, when returning the result of your executed function to the model we recommend passing the matching `id` in your `functionResponse`. If you are using the standard Python or Node.js SDKs, this is handled automatically.

<button value="weather">Get Weather</button> <button value="meeting" default="">Schedule Meeting</button> <button value="chart">Create Chart</button>

### Python

    from google import genai
    from google.genai import types

    # Define the function declaration for the model
    schedule_meeting_function = {
        "name": "schedule_meeting",
        "description": "Schedules a meeting with specified attendees at a given time and date.",
        "parameters": {
            "type": "object",
            "properties": {
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of people attending the meeting.",
                },
                "date": {
                    "type": "string",
                    "description": "Date of the meeting (e.g., '2024-07-29')",
                },
                "time": {
                    "type": "string",
                    "description": "Time of the meeting (e.g., '15:00')",
                },
                "topic": {
                    "type": "string",
                    "description": "The subject or topic of the meeting.",
                },
            },
            "required": ["attendees", "date", "time", "topic"],

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Structured outputs
*Source: /structured-output*

You can configure Gemini models to generate responses that adhere to a provided JSON
Schema. This ensures predictable, type-safe results and simplifies extracting
structured data from unstructured text.

Using structured outputs is ideal for:

- **Data extraction:** Pull specific information like names and dates from text.
- **Structured classification:** Classify text into predefined categories.
- **Agentic workflows:** Generate structured inputs for tools or APIs.

In addition to supporting JSON Schema in the REST API, the Google GenAI SDKs
make it easy to define schemas using
[Pydantic](https://docs.pydantic.dev/latest/) (Python) and
[Zod](https://zod.dev/) (JavaScript).

<button value="recipe" default="">Recipe Extractor</button> <button value="feedback">Content Moderation</button> <button value="recursive">Recursive Structures</button>

This example demonstrates how to extract structured data from text using basic
JSON Schema types like `object`, `array`, `string`, and `integer`.

### Python

    from google import genai
    from pydantic import BaseModel, Field
    from typing import List, Optional

    class Ingredient(BaseModel):
        name: str = Field(description="Name of the ingredient.")
        quantity: str = Field(description="Quantity of the ingredient, including units.")

    class Recipe(BaseModel):
        recipe_name: str = Field(description="The name of the recipe.")
        prep_time_minutes: Optional[int] = Field(description="Optional time in minutes to prepare the recipe.")
        ingredients: List[Ingredient]
        instructions: List[str]

    client = genai.Client()

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Gemini Developer API pricing
*Source: /pricing*

> [!IMPORTANT]
> We have updated our [Terms of Service](https://ai.google.dev/gemini-api/terms).

Start building free of charge with generous limits, then scale up with
prepaid then pay-as-you-go pricing for your production ready applications.

### Free

For developers and small projects getting started with the Gemini API.

- check_circleLimited access to certain models
- check_circleFree input \& output tokens
- check_circleGoogle AI Studio access
- check_circleContent used to improve our products[\*](https://ai.google.dev/gemini-api/terms)

[Get started for Free](https://aistudio.google.com)

### Paid

For production applications that require higher volumes and advanced features.

- check_circleHigher rate limits for production deployments
- check_circleAccess to Context caching
- check_circleBatch API (50% cost reduction)
- check_circleAccess to Google's most advanced models
- check_circleContent **not** used to improve our products[\*](https://ai.google.dev/gemini-api/terms)

[Upgrade to Paid](https://aistudio.google.com/api-keys)

### Enterprise

For large-scale deployments with custom needs for security, support, and compliance, powered by [Gemini Enterprise Agent Platform](https://cloud.google.com/gemini-enterprise-agent-platform).

- check_circleAll features in Paid, plus optional access to:
- check_circleDedicated support channels
- check_circleAdvanced security \& compliance
- check_circleProvisioned throughput
- check_circleVolume-based discounts (based on usage)
- check_circleML ops, model garden and more

[Contact Sales](https://cloud.google.com/contact)

## Gemini 3.1 Pro Preview

*`gemini-3.1-pro-preview` and `gemini-3.1-pro-preview-customtools`*

[Try it in Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-pro-preview)

The latest performance, intelligence, and usability improvements to the best
model family in the world for multimodal understanding,
agentic capabilities, and vibe-coding.

### Standard

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Gemini API libraries
*Source: /libraries*

<br />

> [!IMPORTANT]
> We have updated our [Terms of Service](https://ai.google.dev/gemini-api/terms).

When building with the Gemini API, we recommend using the **Google GenAI SDK** .
These are the official, production-ready libraries that we develop and maintain
for the most popular languages. They are in [General Availability](https://ai.google.dev/gemini-api/docs/libraries#new-libraries) and used in all our official
documentation and examples.

> [!NOTE]
> **Note:** If you're using one of our legacy libraries, we strongly recommend you [migrate](https://ai.google.dev/gemini-api/docs/migrate) to the Google GenAI SDK. Review the [legacy libraries](https://ai.google.dev/gemini-api/docs/libraries#previous-sdks) section for more information. If you're using an AI coding assistant, install the [Gemini API development skill](https://ai.google.dev/gemini-api/docs/coding-agents) to give your agent access to the latest documentation and best practices.

If you're new to the Gemini API, follow our [quickstart guide](https://ai.google.dev/gemini-api/docs/quickstart) to get started.

## Language support and installation

The Google GenAI SDK is available for the Python, JavaScript/TypeScript, Go and
Java languages. You can install each language's library using package managers,
or visit their GitHub repos for further engagement:

### Python

- Library: [`google-genai`](https://pypi.org/project/google-genai)

- GitHub Repository: [googleapis/python-genai](https://github.com/googleapis/python-genai)

- Installation: `pip install google-genai`

### JavaScript

- Library: [`@google/genai`](https://www.npmjs.com/package/@google/genai)

- GitHub Repository: [googleapis/js-genai](https://github.com/googleapis/js-genai)

- Installation: `npm install @google/genai`

### Go

- Library: [`google.golang.org/genai`](https://pkg.go.dev/google.golang.org/genai)

- GitHub Repository: [googleapis/go-genai](https://github.com/googleapis/go-genai)

- Installation: `go get google.golang.org/genai`

### Java

- Library: `google-genai`

- GitHub Repository: [googleapis/java-genai](https://github.com/googleapis/java-genai)

- Installation: If you're using Maven, add the following to your dependencies:

    <dependencies>
      <dependency>
        <groupId>com.google.genai</groupId>
        <artifactId>google-genai</artifactId>
        <version>1.0.0</version>
      </dependency>
    </dependencies>

### C#

- Library: `Google.GenAI`

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────
