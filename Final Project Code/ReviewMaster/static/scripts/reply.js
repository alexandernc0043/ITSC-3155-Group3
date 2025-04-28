function toggleReplyForm(e, id) {
    e.preventDefault(); // Prevent default action of link.
    const form = document.getElementById(`reply-form-${id}`);
    form.classList.toggle('hidden');
}