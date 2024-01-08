from django.db import models

class Topic(models.Model):
    #Un tema sobre el que esta aprendiendo el usuario
    text = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #Devuelve una representacion del modelo como cadena
        return self.text

class Entry(models.Model):
    #Algo especifico aprendido sobre un tema
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self): 
        #Devuelve una representacion del modelo como cadena
        return f"{self.text[:50]}"
