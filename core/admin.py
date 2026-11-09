from django.contrib import admin
from .models import (
    MoodEntry,
    UserProfile,
    OTPVerification,
    LoginActivity,
    UserReadingProgress,
    ReadingAnalytics,
)


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'created_at')
    list_filter = ('mood', 'created_at')
    search_fields = ('user__username', 'mood')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile', 'is_admin', 'is_locked', 'failed_otp_attempts')
    list_filter = ('is_admin', 'is_locked')
    search_fields = ('user__username', 'mobile')


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'purpose', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('purpose', 'is_verified')
    search_fields = ('email', 'user__username')


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'ip_address', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('user__username', 'ip_address')


@admin.register(UserReadingProgress)
class UserReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_key', 'current_page', 'percentage_completed', 'last_read')
    list_filter = ('book_key',)
    search_fields = ('user__username', 'book_key')


@admin.register(ReadingAnalytics)
class ReadingAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_reading_time', 'books_completed', 'reading_streak', 'last_reading_date')
    search_fields = ('user__username',)
