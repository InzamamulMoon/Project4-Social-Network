document.addEventListener("DOMContentLoaded", function () {
  const text_area=document.getElementById("container")

  const make_post=document.getElementById("post_button");

  make_post

  let isReversed = false; // Track the direction of the animation

  // Set the animation duration
  //text_area.style.animationDuration = '2s';

  make_post.onclick = () => {
    container.classList.toggle('active');


    /*if (!isReversed) {
      // Play the animation forwards if it's currently reversed
      text_area.add();
      text_area.style.animationName = 'tweet';
      text_area.style.animationDirection = 'normal';
      text_area.style.animationPlayState = 'running';
    } else {
      // Play the animation in reverse if it's currently forwards
      text_area.style.animationName = 'tweet';
      text_area.style.animationDirection = 'reverse';
      text_area.style.animationPlayState = 'running';
    }

    // Toggle the direction state
    isReversed = !isReversed;

    // Listen for the animation end to pause it
    text_area.addEventListener("animationend", () => {
      text_area.style.animationPlayState = 'paused';
    });
  
   /* if ( text_area.style.animationPlayState === 'paused') {
      text_area.style.animationPlayState = 'running';
    }

// Otherwise, pause the animation
   else {
    text_area.style.animationPlayState = 'paused';
  }*/
};



  var clas = document.getElementsByClassName("form-control");
  var i;
  for (i = 0; i < clas.length; i++) {
    clas[i].style.display = "none";
  }

  document.querySelectorAll("p").forEach(function (p) {
    const id = p.dataset.postid;

    p.addEventListener("click", () => {
      fetch(`/authenticate/${id}`)
        .then((response) => response.json())
        .then((output) => {
          if (output.boolean) {
            editPost(id);
          }
        });
    });
  });

  
    const like_buttons=document.getElementsByClassName("like-button");
   
    window.addEventListener("load", () =>{
    Array.from(like_buttons).forEach(button=>{
      const pri_key=button.dataset.like_id;
      const like_counter=document.getElementById(`likeCount-${pri_key}`);
    
      render_likes(pri_key,button,like_counter);
    

      button.addEventListener("click",function(event){
        event.preventDefault();
        fetch(`/authenticate/${pri_key}`)
        .then((response) => response.json())
        .then((output) => {
          if(!output.boolean) {
            Like_Post(pri_key,button,like_counter)}
      })
    })

 })
})
})


function updateButtonColor(button, isLiked) {
  if (isLiked) {
    button.style.color = "red";
    button.classList.add("red-like-button");
  } else {
    button.style.color = "grey";
    button.classList.remove("red-like-button");
  }
}

function render_likes(pri_key,button,like_counter){
            fetch(`/like/${pri_key}`)
            .then((response)=>response.json())
            .then((result) => {
              like_counter.innerHTML=result.number_of_likes;
              updateButtonColor(button,result.bool_value)
            });
 
}

function Like_Post(pri_key,button,like_counter){

  fetch(`/like/${pri_key}`,{
     method: "POST",
     headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
  }
  })
  .then((response) => response.json())
  .then((result)=>{
    updateButtonColor(button,result.bool_value)
    like_counter.innerHTML=result.number_of_likes;
  })
}
function editPost(id) {
  //var text_content=document.getElementById(`content_${id}`).value;
  document.getElementById(`content_${id}`).style.display = "none";
  document.getElementById(`edit_${id}`).style.display = "block";
  //console.log(text_content);

  const basepath= window.location.pathname.includes('user_profile') ? '/user_profile': '';
  var new_c = document.getElementById(`edit_${id}`);
  console.log(id);
  fetch(`${basepath}/edit/${id}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(`edit_${id}`).value = `${data.content}`;
    });

  new_c.addEventListener("keyup", function (event) {
    event.preventDefault();

    if (event.key === "Enter") {
      const edited_post = document.getElementById(`edit_${id}`).value;
      fetch(`${basepath}/edit_post/`, {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
      },
        body: JSON.stringify({
          post_content: edited_post,
          pk: id,
        }),
      });

      document.getElementById(`edit_${id}`).style.display = "none";
      document.getElementById(`content_${id}`).innerHTML=edited_post;
      document.getElementById(`content_${id}`).style.display = "block";
    }
  });
}

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
 }


