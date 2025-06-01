<template>
  <div class="chat-container">
    <h2>Real-time Chat</h2>

    <div class="user-setup" v-if="!connected">
      <input v-model="username" placeholder="Unesi korisničko ime" />
      <button @click="connect">Spoji se</button>
    </div>

    <div class="chat-box" v-else>
      <div class="messages">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <strong>{{ msg.username }}:</strong> {{ msg.message }}
        </div>
      </div>
      <div class="input-area">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Unesi poruku"
        />
        <button @click="sendMessage">Pošalji</button>
      </div>
    </div>
  </div>
</template>
