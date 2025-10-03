function loadTodos() {
    const todosJSON = localStorage.getItem('susnata-todos');
    return todosJSON ? JSON.parse(todosJSON) : [];
}

function saveTodos(todos) {
    localStorage.setItem('susnata-todos', JSON.stringify(todos));
}

function renderTodos() {
    const todoList = document.getElementById('todo-list');
    const todos = loadTodos();
    
    todoList.innerHTML = '';
    
    todos.forEach(todo => {
        const li = document.createElement('li');
        
        const span = document.createElement('span');
        span.textContent = todo.text;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.setAttribute('data-id', todo.id);
        deleteBtn.textContent = 'Delete';
        
        li.appendChild(span);
        li.appendChild(deleteBtn);
        todoList.appendChild(li);
    });
}

function addTodo() {
    const input = document.getElementById('todo-input');
    const text = input.value.trim();
    
    if (text === '') {
        return;
    }
    
    const todos = loadTodos();
    const newTodo = {
        id: Date.now(),
        text: text
    };
    
    todos.push(newTodo);
    saveTodos(todos);
    renderTodos();
    input.value = '';
}

function deleteTodo(id) {
    const todos = loadTodos();
    const filteredTodos = todos.filter(todo => todo.id !== id);
    saveTodos(filteredTodos);
    renderTodos();
}

document.getElementById('add-btn').addEventListener('click', addTodo);

document.getElementById('todo-list').addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-btn')) {
        const id = parseInt(event.target.getAttribute('data-id'));
        deleteTodo(id);
    }
});

const todos = loadTodos();
renderTodos();