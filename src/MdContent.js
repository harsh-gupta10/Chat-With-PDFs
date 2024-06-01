import React from 'react';
import MarkdownRenderer from './MarkdownRenderer';
import { CopyBlock, dracula } from 'react-code-blocks';

// Function to process the content
const processContent = (originalContent) => {
  const codeBlockPattern = /```(\w*)\n(.*?)\n```/gs;
  let match;
  let lastIndex = 0;
  const parts = [];

  while ((match = codeBlockPattern.exec(originalContent)) !== null) {
    // Text before the code block
    const textPart = originalContent.slice(lastIndex, match.index);
    if (textPart.trim()) {
      parts.push({ text: textPart, code: null });
    }

    // The code block
    const codePart = match[2];
    parts.push({ text: null, code: codePart });

    lastIndex = match.index + match[0].length;
  }

  // Text after the last code block
  const textPart = originalContent.slice(lastIndex);
  if (textPart.trim()) {
    parts.push({ text: textPart, code: null });
  }

  return parts;
};

function MyCoolCodeBlock({ code, language, showLineNumbers }) {
  return (
    <CopyBlock
      text={code}
      language={language}
      showLineNumbers={showLineNumbers}
      theme={dracula}
      codeBlock
    />
  );
}

const MdContent = () => {
  const originalContent = `A linked list in C++ is a linear data structure, composed of nodes that contain an element and a reference (pointer) to the next node in the sequence. The first node is called the head or the beginning, and the last node's next pointer points to \`nullptr\`. Unlike arrays, where elements are adjacent in memory, linked lists allow for greater flexibility as they can be dynamically allocated during runtime, enabling efficient insertion into the middle of the list without having to relocate many items.

In C++, you typically define a struct or class to represent each node in the linked list, with pointers pointing to the data element and the next node. Here's an example:

\`\`\`cpp
struct Node {
    int data;
    Node * next;
};
\`\`\`

The \`next\` pointer can be initialized as \`nullptr\` or to point to another node in the list during the creation of each new node. You can traverse the linked list by starting from the first (or head) node and following the next pointers. The time complexity for search operations is linear, O(N), since you have to examine at most N nodes during a search.

To create a cycle in the linked list, you can set the \`next\` pointer of a node to another node that has already been allocated. If you follow this next link from any given node and end up returning to the starting point, then the linked list contains a cycle. This can be useful for solving certain problems, such as detecting cycles in the list or finding its length.

The linked list is an efficient data structure when dealing with dynamic situations where the size of the collection is uncertain or frequently changing. It's particularly beneficial when dealing with large amounts of data or insertions and deletions at arbitrary positions within the sequence.
\`\`\`cpp
struct Node {
    int data;
    Node * next;
};
\`\`\`
`;

  const parts = processContent(originalContent);

  return (
    <div className="MdContent">
      <h1>Markdown Example</h1>
      {parts.map((part, index) => (
        <div key={index}>
          {part.text && <MarkdownRenderer markdown={part.text} />}
          {part.code && <MyCoolCodeBlock code={part.code} language="cpp" showLineNumbers={true} />}
        </div>
      ))}
    </div>
  );
};

export default MdContent;
