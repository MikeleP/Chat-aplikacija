<template>
  <div>
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <h2>Upiši svoje ime:</h2>
        <input v-model="usernameInput" @keyup.enter="confirmUsername" />
        <button @click="confirmUsername">Uđi u chat</button>
      </div>
    </div>

    <div class="chat-wrapper" v-else>
      <div class="chat-log">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="msg.type === 'system' ? 'system-msg' : 'chat-bubble'"
        >
          {{ msg.text }}
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Upiši poruku..."
        />
        <button @click="sendMessage">Pošalji</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const showModal = ref(true);
const usernameInput = ref("");
const messages = ref([{ text: "Dobrodošao u Chat sobu", type: "system" }]);
const newMessage = ref("");
let username = "";
const socket = ref(null);

function confirmUsername() {
  if (!usernameInput.value.trim()) return;

  username = usernameInput.value.trim();
  showModal.value = false;

  socket.value = new WebSocket("ws://localhost:8000/ws");

  socket.value.onopen = () => {
    socket.value.send(
      JSON.stringify({
        username: username,
        message: "__joined__",
      })
    );
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.message === "__joined__") {
      messages.value.push({
        text: `${data.username} se pridružio Chat-u`,
        type: "system",
      });
    } else if (data.message === "__left__") {
      messages.value.push({
        text: `${data.username} je napustio Chat.`,
        type: "system",
      });
    } else {
      messages.value.push({
        text: `${data.username}: ${data.message}`,
        type: "user",
      });
    }
  };

  socket.value.onclose = () => {
    messages.value.push({ text: "Veza prekinuta", type: "system" });
  };
}

function sendMessage() {
  if (!newMessage.value || !socket.value) return;

  const msg = {
    username: username,
    message: newMessage.value,
  };

  socket.value.send(JSON.stringify(msg));
  newMessage.value = "";
}
</script>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ddd;
  font-family: monospace;
}

.chat-log {
  flex-grow: 1;
  padding: 10px;
  overflow-y: auto;
}

.chat-input {
  padding: 10px;
  display: flex;
  gap: 10px;
  background: #fff;
}

.chat-input input {
  flex: 1;
  padding: 10px 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 999px;
  outline: none;
}

.chat-input button {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  background-color: darkblue;
  color: #fff;
  border-radius: 999px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #333;
}

.system-msg {
  text-align: center;
  color: #555;
  font-style: italic;
  margin: 5px 0;
}

.chat-bubble {
  background-color: lightblue;
  border-radius: 999px;
  padding: 12px 20px;
  margin: 6px 0;
  font-size: 1.1rem;
  max-width: fit-content;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.modal {
  background: white;
  padding: 30px 40px;
  border-radius: 16px;
  text-align: center;
  font-size: 1.2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.modal input {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 10px;
  width: 100%;
}

.modal button {
  margin-top: 15px;
  padding: 10px 20px;
  background: darkblue;
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-size: 1rem;
}
</style>
