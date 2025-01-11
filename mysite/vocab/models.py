from django.db import models
from django.conf import settings
from datetime import date
import random
from courses.models import FutureLesson 


from studentmemberships.models import StudentMembership

def get_days_so_far():
    return (date.today() - date(2020,9,20)).days

# Create your models here.
class VocabularyWord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, blank=True)
    new_word = models.CharField(null=True, max_length=100)
    definition = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wordgrade = models.IntegerField(null=True, blank=True)    
    current_interval = models.IntegerField(default=0)
    easiness = models.FloatField(default=2.5)
    next_rep_day = models.IntegerField(default=0)
    retention_reps_since_lapse = models.IntegerField(default=0)
    lesson = models.ForeignKey(FutureLesson, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __unicode__(self):
        return "Id: %i, Student: %s, Q: %s, A: %s, wordgrade %s, current_interval %i, easiness %f, next_rep_day %i" % \
            (self.id, self.student, self.new_word, self.definition, self.wordgrade, self.current_interval, self.easiness, self.next_rep_day)

    def as_dict(self):
        d = self.__dict__.copy()
        del d['_state']
        return d

    def process_answer(self, new_wordgrade):
        if self.wordgrade == None:
            interval = self.__calculate_initial_interval(new_wordgrade)
        else:
            interval = self.__get_new_interval(new_wordgrade)
        
        interval += self.__calculate_interval_noise(interval)
        
        self.current_interval = interval
        self.next_rep_day = get_days_so_far() + interval
        self.wordgrade = new_wordgrade

    def __get_new_interval(self, new_wordgrade):
        if self.wordgrade in [0,1] and new_wordgrade in [0, 1]:
            return 0
        elif self.wordgrade in [0,1] and new_wordgrade in [2,3,4,5]:
            return 1
        elif self.wordgrade in [2,3,4,5] and new_wordgrade in [0,1]:
            self.retention_reps_since_lapse = 0
            return 1
        elif self.wordgrade in [2,3,4,5] and new_wordgrade in [2,3,4,5]:
            self.retention_reps_since_lapse += 1
            return self.__get_interval_for_remember_both_times(new_wordgrade)
        raise Exception("Invalid wordgrade combination")

    def __get_interval_for_remember_both_times(self, new_wordgrade):
        self.__adjust_easiness(new_wordgrade)
        if self.retention_reps_since_lapse == 1:
            return 6
        elif new_wordgrade in [2, 3]:
            return self.current_interval
        elif new_wordgrade in [4, 5]:
            return self.current_interval * self.easiness
        raise Exception("Invalid new_wordgrade")

    def __adjust_easiness(self, new_wordgrade):
        if new_wordgrade == 2:
            self.easiness -= 0.16
        elif new_wordgrade == 3:
            self.easiness -= 0.14
        elif new_wordgrade == 5:
            self.easiness += 0.10
        
        if self.easiness < 1.3:
            self.easiness = 1.3
            
    def __calculate_interval_noise(self, interval):
        if interval == 0:
            return 0
        elif interval == 1:
            return random.randint(0,1)
        elif interval <= 10:
            return random.randint(-1,1)
        elif interval <= 60:
            return random.randint(-3,3)
        else:
            a = .05 * interval
            return round(random.uniform(-a,a))
        
    def __calculate_initial_interval(self, wordgrade):
        interval = (0, 0, 1, 3, 4, 5) [wordgrade]
        return interval    

    def __str__(self):
        template = '{0.student} {0.new_word}'
        return template.format(self)

