const API_BASE = "http://localhost:5000";

function el(id){return document.getElementById(id)}

function getToken(){ return sessionStorage.getItem('admin_token') }

async function doLogin(username, password){
  const res = await fetch(API_BASE + '/admin/login', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password}) });
  return res.json();
}

el('loginBtn').onclick = async () => {
  el('loginError').textContent = '';
  const username = el('username').value;
  const password = el('password').value;
  try{
    const data = await doLogin(username, password);
    if(data.success && data.token){
      sessionStorage.setItem('admin_token', data.token);
      el('loginBox').classList.add('hidden');
      el('panel').classList.remove('hidden');
      loadQuestions();
    } else {
      el('loginError').textContent = data.error || 'Login failed';
    }
  }catch(e){ el('loginError').textContent = e.message }
}

el('logoutBtn').onclick = async () => {
  const token = getToken();
  try{
    await fetch(API_BASE + '/admin/logout', { method:'POST', headers: token ? {'Authorization': 'Bearer '+token} : {} });
  }catch(e){}
  sessionStorage.removeItem('admin_token');
  el('panel').classList.add('hidden');
  el('loginBox').classList.remove('hidden');
}

async function loadQuestions(){
  el('qaList').innerHTML = 'Loading...';
  try{
    const token = getToken();
    const headers = token ? {'Authorization': 'Bearer '+token} : {};
    const res = await fetch(API_BASE + '/admin/questions', { headers });
    const data = await res.json();
    if(!data.success){ el('qaList').textContent = data.error || 'Error'; return }
    renderList(data.questions || []);
  }catch(e){ el('qaList').textContent = e.message }
}

function renderList(items){
  const container = el('qaList');
  container.innerHTML = '';
  items.forEach(it => {
    const row = document.createElement('div'); row.className='qa';
    const q = document.createElement('textarea'); q.value = it.question; q.rows = 2;
    const a = document.createElement('textarea'); a.value = it.answer; a.rows = 3;
    const meta = document.createElement('div'); meta.className='meta'; meta.textContent = `Category: ${it.category || 'general'} — id: ${it.id}`;
    const save = document.createElement('button'); save.textContent = 'Save';
    save.onclick = async () => {
      const payload = { question: q.value, answer: a.value, category: it.category };
      try{
        const token = getToken();
        const headers = Object.assign({'Content-Type':'application/json'}, token ? {'Authorization':'Bearer '+token} : {});
        const res = await fetch(API_BASE + '/admin/question/' + it.id, { method:'PUT', headers: headers, body: JSON.stringify(payload)});
        const data = await res.json();
        if(data.success){ el('adminMsg').textContent = 'Updated'; setTimeout(()=>el('adminMsg').textContent='',1500)} else { el('adminMsg').textContent = data.error }
      }catch(e){ el('adminMsg').textContent = e.message }
    }
    row.appendChild(meta); row.appendChild(q); row.appendChild(a); row.appendChild(save);
    container.appendChild(row);
  })
}

el('addBtn').onclick = async () => {
  const q = el('newQ').value; const a = el('newA').value; const cat = el('newCat').value || 'general';
  if(!q || !a){ el('adminMsg').textContent = 'Question and answer required'; return }
  try{
    const token = getToken();
    const headers = Object.assign({'Content-Type':'application/json'}, token ? {'Authorization':'Bearer '+token} : {});
    const res = await fetch(API_BASE + '/admin/question', { method:'POST', headers: headers, body: JSON.stringify({question:q,answer:a,category:cat}) });
    const data = await res.json();
    if(data.success){ el('adminMsg').textContent = 'Added'; el('newQ').value=''; el('newA').value=''; loadQuestions(); }
    else el('adminMsg').textContent = data.error || 'Error'
  }catch(e){ el('adminMsg').textContent = e.message }
}

// on load, keep admin logged in for the tab if token exists
document.addEventListener('DOMContentLoaded', () => {
  const token = getToken();
  if(token){
    el('loginBox').classList.add('hidden');
    el('panel').classList.remove('hidden');
    loadQuestions();
  } else {
    el('loginBox').classList.remove('hidden');
    el('panel').classList.add('hidden');
  }
});
