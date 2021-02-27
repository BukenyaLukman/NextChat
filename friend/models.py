from django.db import models
from django.conf import settings
from django.utils import timezone


class FriendList(models.Model):
	user				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends 				= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name="Friends")

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add A new Friend
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			

	def remove_friend(self,account):
		"""
		Remove a friend
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone
		"""
		remover_friend_list =  self # person terminating the friendship

		# Remove friend from friend request
		remover_friend_list.remove_friend(removee)

		# Remove friend from the removeee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(self.user)

	def is_mutual_friend(self, friend):

		""" Is this a friend ? """
		if friend in self.friends.all():
			return True
		return False

class FriendRequest(models.Model):
	sender					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
	is_active				= models.BooleanField(blank=True, null=False, default=True)
	timestamp				= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.sender.username

	def accept(self):
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list =  FriendList.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		self.is_active = False
		self.save()

	def cancel(self):
		# cancel Friend Request
		# It is cancelled by setting the is_active field to False
		self.is_active = False
		self.save()