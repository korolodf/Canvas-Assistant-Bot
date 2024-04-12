<App>
  <Include src="./functions.rsx" />
  <Frame
    id="$main"
    enableFullBleed={true}
    isHiddenOnDesktop={false}
    isHiddenOnMobile={false}
    padding="8px 12px"
    sticky={null}
    type="main"
  >
    <Container
      id="container1"
      footerPadding="4px 12px"
      headerPadding="4px 12px"
      padding="12px"
      showBody={true}
      showBorder={false}
      showHeader={true}
    >
      <Header>
        <Image
          id="image1"
          horizontalAlign="center"
          retoolStorageFileId="a4ec51aa-79aa-4a7f-af58-c1f9e1490894"
          src="https://placekitten.com/400/300"
          srcType="retoolStorageFileId"
        />
      </Header>
      <View id="82dce" viewKey="View 1">
        <Text
          id="text1"
          value="👋 **Hello {{ current_user.firstName || 'friend' }}!**
Hi I’m Chatterbox, your personalized Canvas helper. Please feel free to ask me any questions you might about this course, including assignment due dates, weekly announcements, or syllabus related concerns"
          verticalAlign="center"
        />
        <Chat
          id="chat1"
          _actionDisabled={{ ordered: [{ "1a": "" }] }}
          _actionHidden={{ ordered: [{ "1a": "" }] }}
          _actionIcon={{ ordered: [{ "1a": "line/interface-align-front" }] }}
          _actionIds={["1a"]}
          _actionLabel={{ ordered: [{ "1a": "Copy" }] }}
          _actionType={{ ordered: [{ "1a": "copy" }] }}
          _defaultUsername="{{ current_user.fullName }}"
          _headerButtonHidden={{ ordered: [{ "2b": "" }, { "3c": "" }] }}
          _headerButtonIcon={{
            ordered: [
              { "2b": "line/interface-download-button-2" },
              { "3c": "line/interface-delete-bin-2" },
            ],
          }}
          _headerButtonIds={["2b", "3c"]}
          _headerButtonLabel={{
            ordered: [{ "2b": "Download" }, { "3c": "Clear history" }],
          }}
          _headerButtonType={{
            ordered: [{ "2b": "download" }, { "3c": "clearHistory" }],
          }}
          _sessionStorageId="a27d0d15-7308-4978-89b3-45d0dd458f4c"
          assistantName="ChatterBox"
          avatarFallback="{{ current_user.fullName }}"
          avatarImageSize={32}
          avatarSrc="{{ current_user.profilePhotoUrl }}"
          emptyDescription="Send a message to chat with AI"
          emptyTitle="No messages here yet"
          margin="0"
          placeholder="Type a message"
          queryTargetId="chat1_query1"
          showAvatar={true}
          showEmptyState={true}
          showHeader={true}
          showTimestamp={true}
          style={{ ordered: [{ background: "automatic" }] }}
          title="Chat"
        >
          <Event
            event="submit"
            method="trigger"
            params={{ ordered: [] }}
            pluginId="chat1_query1"
            type="datasource"
            waitMs="0"
            waitType="debounce"
          />
          <Event
            event="clickAction"
            method="copyToClipboard"
            params={{ ordered: [{ value: "{{ currentMessage.value }}" }] }}
            pluginId="chat1"
            targetId="1a"
            type="util"
            waitMs="0"
            waitType="debounce"
          />
          <Event
            event="clickHeader"
            method="exportData"
            pluginId="chat1"
            targetId="2b"
            type="widget"
            waitMs="0"
            waitType="debounce"
          />
          <Event
            event="clickHeader"
            method="clearHistory"
            pluginId="chat1"
            targetId="3c"
            type="widget"
            waitMs="0"
            waitType="debounce"
          />
        </Chat>
      </View>
    </Container>
  </Frame>
</App>
