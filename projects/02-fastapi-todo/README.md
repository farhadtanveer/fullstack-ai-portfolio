<script src="https://tracking.paqato.com/scripts/pqt-tracking.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
    var notepadEntry = document.querySelector('.navigation--entry.entry--notepad');
    
    if (notepadEntry) {
        var li = document.createElement('li');
        li.className = 'navigation--entry';
        li.innerHTML = '<a href="shopware.php?sViewport=forms&sFid=23" class="btn is--icon-left entry--link account--link btn--widerruf" title="Vertrag widerrufen"><i class="icon--emotion"></i><span class="account--display">Vertrag widerrufen</span></a>';
        notepadEntry.parentNode.insertBefore(li, notepadEntry);
    }
});
</script>

<!-- new scripts -->

<script>
document.addEventListener("DOMContentLoaded", function() {

    var returnLink = document.querySelector('a[href="https://www.kuechexxl.de/custom/index/sCustom/53"]');

    if (returnLink) {

        var warrantyContainer = document.createElement('div');

        warrantyContainer.style.marginTop = "15px";
        warrantyContainer.style.padding = "10px";
        warrantyContainer.style.border = "1px solid #ddd";
        warrantyContainer.style.borderRadius = "5px";
        warrantyContainer.style.background = "#fafafa";

        warrantyContainer.innerHTML = `
            <a href="https://www.kuechexxl.de/media/image/be/30/ef/Legal-guarantee_notice_DE.jpg" 
               target="_blank"
               style="display:block; font-weight:bold; margin-bottom:10px;">
                Informationen zur Garantie
            </a>

            <a href="https://www.kuechexxl.de/media/image/be/30/ef/Legal-guarantee_notice_DE.jpg" 
               target="_blank">
                <img src="https://www.kuechexxl.de/media/image/be/30/ef/Legal-guarantee_notice_DE.jpg"
                     alt="Garantie Informationen"
                     style="width:120px; height:auto; border:1px solid #ccc; cursor:pointer;">
            </a>
        `;

        returnLink.parentNode.insertBefore(warrantyContainer, returnLink.nextSibling);

    }

});
</script>
