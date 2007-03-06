from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Group(models.Model):
    name = models.CharField(_('Group Name'), maxlength=80)
    description = models.TextField(_('Description'), blank=True)
    icon = models.ImageField(_('Icon'), upload_to='groups', blank=True)
    managers = models.ManyToManyField(User, related_name="managers")
    members = models.ManyToManyField(User, related_name="members")
    public = models.BooleanField(default=True)  #group is public or private
    freejoin = models.BooleanField(default=True)#group can free join in
    
    def __str__(self):
        return self.name
    
    class Admin: pass
    
    def get_managers(self):
        s = []
        for m in self.managers.all():
            s.append(m.username)
        return ' '.join(s)
    
    def is_manager(self, user):
        if user.is_anonymous():
            return False
        if user.is_superuser or self.managers.filter(username=user.username):
            return True
        else:
            return False
        
    def is_member(self, user):
        if user.is_anonymous():
            return False
        if self.is_manager(user) or self.members.filter(username=user.username):
            return True
        else:
            return False 
        
    def add_member(self, user):
        if not self.is_member(user):
            self.members.add(user)
            
    def del_member(self, user):
        if self.is_member(user):
            self.members.remove(user)
    
class UserProfile(models.Model):
    portrait = models.ImageField(_('Photo'), upload_to='photo', blank=True)
    user = models.ForeignKey(User, unique=True)
    
    def __str__(self):
        return self.user.username

    class Admin: pass

    def get_portrait(self):
        if self.portrait:
            return self.get_portrait_url()
        else:
            return 'img/user.jpg'