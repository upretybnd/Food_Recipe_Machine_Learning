from django.shortcuts import render
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Load model and tokenizer
model_name = 'facebook/blenderbot-400M-distill'
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)


def chatbot_view(request):
    response = ''
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        inputs = tokenizer([user_input], return_tensors='pt')
        reply_ids = model.generate(**inputs)
        response = tokenizer.decode(reply_ids[0], skip_special_tokens=True)

    return render(request, 'chatbot/chat.html', {'response': response})
