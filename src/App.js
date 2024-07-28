import React, { useState } from 'react';
import './App.css';

function App() {
  const [todo, settodo] = useState([]);
  const [latesttodo, setlatesttodo] = useState('');
  const [ModifytodoId, setModifytodoId] = useState(null);
  const [ModifytodoText, setModifytodoText] = useState('');

  const addtodo = () => {
    if (latesttodo.trim() !== '') {
      settodo([...todo, { id: Date.now(), text: latesttodo }]);
      setlatesttodo('');
    }
  };

  const Removetodo = (id) => {
    settodo(todo.filter(todo => todo.id !== id));
  };

  const beginModifytodo = (id, text) => {
    setModifytodoId(id);
    setModifytodoText(text);
  };

  const storetodo = (id) => {
    settodo(todo.map(todo => (todo.id === id ? { ...todo, text: ModifytodoText } : todo)));
    setModifytodoId(null);
    setModifytodoText('');
  };

  return (
    <div className="App">
      <h1>To-Do List</h1>
      <div>
        <input
          type="text"
          placeholder="Add a latest todo"
          value={latesttodo}
          onChange={(e) => setlatesttodo(e.target.value)}
        />
        <button onClick={addtodo}>Add todo</button>
      </div>
      <ul>
        {todo.map(todo => (
          <li key={todo.id}>
            {ModifytodoId === todo.id ? (
              <div>
                <input
                  type="text"
                  value={ModifytodoText}
                  onChange={(e) => setModifytodoText(e.target.value)}
                />
                <button onClick={() => storetodo(todo.id)}>store</button>
              </div>
            ) : (
              <div>
                {todo.text}
                <button onClick={() => beginModifytodo(todo.id, todo.text)}>Modify</button>
                <button onClick={() => Removetodo(todo.id)}>Remove</button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;